from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from AppHome.forms import RegisterForm
from AppHome.models import Folder, File
from AppUser.models import CustomUser


# Create your views here.
class IndexView(View):
    template_name = 'file-manager.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(self.request)
        else:
            return redirect('login')

    def get(self, request):
        root_folders = Folder.objects.filter(parent__isnull=True, is_del=False)
        root_files = File.objects.filter(parent__isnull=True, is_del=False)

        context = {
            'folders': root_folders,
            'files': root_files,
            'parent_rec_id': '',
            'total_size_mb': get_allover_size(request),
            'parent_folder': None,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        action = request.POST.get('action', None)
        parent_rec_id = request.POST.get('parent_rec_id', None)
        if action == 'open-folder':
            rec_id = request.POST.get('rec_id', '')
            if rec_id:
                try:
                    obj = Folder.objects.get(id=rec_id, is_del=False)

                    folders = Folder.objects.filter(parent=obj, is_del=False)
                    files = File.objects.filter(parent=obj, is_del=False)
                    context = {
                        'folders': folders,
                        'files': files,
                        'parent_rec_id': rec_id,
                        'total_size_mb': get_allover_size(request),
                        'parent_folder': obj,
                    }
                    return render(request, self.template_name, context=context)
                except Exception as e:
                    print(e)
        elif action == 'create-folder':
            folder_name = request.POST.get('folder_name', '').strip()
            parent_rec_id = request.POST.get('parent_rec_id', '')
            extra_param = {}

            if parent_rec_id:
                extra_param['parent_id'] = parent_rec_id

            if not folder_name:
                messages.error(request, 'Please enter Folder Name')
            else:
                try:
                    if Folder.objects.filter(name=folder_name, **extra_param).exists():
                        messages.error(request, f'Folder "{folder_name}" already exists in this location.')
                    else:
                        new_obj = Folder.objects.create(name=folder_name, **extra_param, author=request.user)

                        if parent_rec_id:
                            parent_obj = Folder.objects.get(id=parent_rec_id, is_del=False)

                            folders = Folder.objects.filter(parent=parent_obj, is_del=False)
                            files = File.objects.filter(parent=parent_obj, is_del=False)
                        else:
                            folders = Folder.objects.filter(parent__isnull=True, is_del=False)
                            files = File.objects.filter(parent__isnull=True, is_del=False)
                            parent_rec_id = ''

                        context = {
                            'folders': folders,
                            'files': files,
                            'parent_rec_id': parent_rec_id,
                            'total_size_mb': get_allover_size(request),
                            'parent_folder': parent_obj,
                        }
                        messages.success(request, f'{folder_name} created successfully!')
                        return render(request, self.template_name, context)
                except Folder.DoesNotExist:
                    messages.error(request, 'The parent folder does not exist.')
                except IntegrityError:
                    messages.error(request, f'An error occurred while creating the folder "{folder_name}".')
            return redirect('index')
        elif action == 'rename-folder':
            folder_name = request.POST.get('folder_name', '').strip()
            folder_id = request.POST.get('rec_id', None)

            if not folder_name:
                messages.error(request, 'Please enter a new Folder Name')
            else:
                try:
                    folder_to_rename = Folder.objects.get(id=folder_id, is_del=False)
                    extra_param = {}
                    if folder_to_rename.parent:
                        extra_param['parent'] = folder_to_rename.parent
                    if Folder.objects.filter(name=folder_name, is_del=False, **extra_param).exclude(
                            id=folder_id).exists():
                        messages.error(request, f'Folder "{folder_name}" already exists in this location.')
                        return redirect('index')

                    folder_to_rename.name = folder_name
                    folder_to_rename.save()
                    messages.success(request, f'Folder renamed to "{folder_name}" successfully!')

                    parent_obj = folder_to_rename.parent
                    if parent_obj:
                        folders = Folder.objects.filter(parent=parent_obj, is_del=False)
                    else:
                        folders = Folder.objects.filter(parent__isnull=True, is_del=False)
                    files = File.objects.filter(parent=parent_obj, is_del=False)

                    context = {
                        'folders': folders,
                        'files': files,
                        'parent_rec_id': parent_obj.id if parent_obj else '',
                        'total_size_mb': get_allover_size(request),
                        'parent_folder': parent_obj,
                    }
                    return render(request, self.template_name, context=context)
                except Folder.DoesNotExist:
                    messages.error(request, 'The folder does not exist.')

            return redirect('index')
        elif action == 'delete-folder':
            folder_id = request.POST.get('rec_id', None)

            try:
                folder_to_delete = Folder.objects.get(id=folder_id, is_del=False)
                parent_obj = folder_to_delete.parent

                if folder_to_delete.folders.exists() or folder_to_delete.files.exists():
                    messages.error(request,
                                   f'Folder "{folder_to_delete.name}" is not empty. Please delete its contents first.')
                else:
                    folder_to_delete.is_del = True  # Mark the folder as deleted
                    folder_to_delete.save()
                    messages.success(request, f'Folder "{folder_to_delete.name}" deleted successfully!')

                if parent_obj:
                    folders = Folder.objects.filter(parent=parent_obj, is_del=False)
                else:
                    folders = Folder.objects.filter(parent__isnull=True, is_del=False)
                files = File.objects.filter(parent=parent_obj, is_del=False)

                context = {
                    'folders': folders,
                    'files': files,
                    'parent_rec_id': parent_obj.id if parent_obj else '',
                    'total_size_mb': get_allover_size(request),
                    'parent_folder': parent_obj,
                }
                return render(request, self.template_name, context=context)
            except Folder.DoesNotExist:
                messages.error(request, 'The folder does not exist.')
        elif action == 'upload-file':

            try:
                uploaded_file = request.FILES.get('file')
                file_extension = uploaded_file.name.split('.')[-1]

                file_size = uploaded_file.size
                param = {
                    'name': uploaded_file.name,
                    'author': request.user,
                    'document': uploaded_file,
                    'extension': file_extension,
                    'size': file_size,
                }
                if parent_rec_id:
                    param['parent_id'] = parent_rec_id
                if not uploaded_file:
                    messages.error(request, 'No file selected for upload.')
                else:

                    new_file = File.objects.create(**param)
                    messages.success(request, f'File "{uploaded_file.name}" uploaded successfully!')
            except Folder.DoesNotExist:
                messages.error(request, 'The parent folder does not exist.')

            if parent_rec_id:
                parent_obj = Folder.objects.get(id=parent_rec_id, is_del=False)
                folders = Folder.objects.filter(parent=parent_obj, is_del=False)
            else:
                parent_obj = None
                folders = Folder.objects.filter(parent__isnull=True, is_del=False)

            files = File.objects.filter(parent=parent_obj, is_del=False)

            context = {
                'folders': folders,
                'files': files,
                'parent_rec_id': parent_obj.id if parent_obj else '',
                'total_size_mb': get_allover_size(request),
                'parent_folder': parent_obj,
            }
            return render(request, self.template_name, context=context)
        elif action == 'fetch-file':
            parent_rec_id = request.POST.get('parent_rec_id', '')
            file_id = request.POST.get('rec_id', None)
            file_to_fetch = None

            if not file_id:
                messages.error(request, 'File not specified for fetching details.')
            else:
                try:
                    file_to_fetch = File.objects.get(id=file_id, is_del=False)
                except File.DoesNotExist:
                    messages.error(request, 'The file does not exist.')

            if parent_rec_id:
                parent_obj = Folder.objects.get(id=parent_rec_id, is_del=False)
                folders = Folder.objects.filter(parent=parent_obj, is_del=False)
            else:
                parent_obj = None
                folders = Folder.objects.filter(parent__isnull=True, is_del=False)

            files = File.objects.filter(parent=parent_obj, is_del=False)

            context = {
                'folders': folders,
                'files': files,
                'parent_rec_id': parent_obj.id if parent_obj else '',
                'file_to_fetch': file_to_fetch,
                'total_size_mb': get_allover_size(request),
                'parent_folder': parent_obj,
            }
            return render(request, self.template_name, context=context)
        elif action == 'delete-file':
            file_id = request.POST.get('rec_id')
            if file_id:
                try:
                    file_to_delete = File.objects.get(id=file_id, is_del=False)

                    file_to_delete.is_del = True
                    file_to_delete.save()
                    messages.success(request, f'File "{file_to_delete.name}" deleted successfully!')
                except File.DoesNotExist:
                    messages.error(request, 'The file does not exist.')
            else:
                messages.error(request, 'Something went wrong')

            if parent_rec_id:
                parent_obj = Folder.objects.get(id=parent_rec_id, is_del=False)
                folders = Folder.objects.filter(parent=parent_obj, is_del=False)
            else:
                parent_obj = None
                folders = Folder.objects.filter(parent__isnull=True, is_del=False)

            files = File.objects.filter(parent=parent_obj, is_del=False)

            context = {
                'folders': folders,
                'files': files,
                'parent_rec_id': parent_obj.id if parent_obj else '',
                'total_size_mb': get_allover_size(request),
                'parent_folder': parent_obj,
            }
            return render(request, self.template_name, context=context)
        return redirect('index')


class DownloadFileView(View):
    def get(self, request, file_id):
        file_obj = get_object_or_404(File, id=file_id, is_del=False)

        response = HttpResponse(file_obj.document, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'

        return response


class SignUpView(CreateView):
    model = CustomUser
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    fields = ['username', 'password', 'email', 'phone_number']

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', context={'error': form.errors})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')


def get_allover_size(request, size_in="MB"):
    total_size = File.objects.filter(is_del=False).aggregate(total_size=Sum('size'))['total_size']
    if total_size:
        size_ratio = (total_size * 100)/(1024 * 1024 * 1024) # ratio in compare to 1GB total size
        if size_in == "MB":
            total_size = total_size / (1024 * 1024)
    else:
        total_size = 0
        size_ratio = 0
    data = {
        'total_size': "{:.2f}".format(total_size),
        'size_ratio': size_ratio,
    }
    return data
