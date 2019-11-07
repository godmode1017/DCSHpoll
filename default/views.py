from django.shortcuts import render
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse

## Create your views here.
## 投票主題列表
class PollList(ListView):
    model = Poll
## 投票主題檢視
class PollDetail(DetailView):
    model = Poll
    # 取得額外資料供頁面範本顯示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        options = Option.objects.filter(poll_id=self.kwargs['pk'])
        context['options'] = options
        return context
 
 ## 投票
class PollVote(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        option = Option.objects.get(id=self.kwargs['pk'])
        option.count += 1   # 將選項的票數+1
        option.save()       # 儲存至資料庫
        return "/poll/"+str(option.poll_id)+"/"       
        
        ## 新增投票主題
class PollCreate(CreateView):
    model = Poll
    fields = ['subject']    # 指定要顯示的欄位
    success_url = '/poll/'  # 成功新增後要導向的路徑
    template_name = 'general_form.html' # 要使用的頁面範本

    ## 修改投票主題
class PollUpdate(UpdateView):
    model = Poll
    fields = ['subject']        # 指定要顯示的欄位
    success_url = '/poll/'      # 成功新增後要導向的路徑
    template_name = 'general_form.html' # 要使用的頁面範本

    ## 刪除投票主題
class PollDelete(DeleteView):
    model = Poll
    success_url = '/poll/'
    template_name = "confirm_delete.html"

    ## 新增投票選項
class OptionCreate(CreateView):
    model = Option
    fields = ['title']
    template_name = 'general_form.html'
    # 成功新增選項後要導向其所屬的投票主題檢視頁面
    def get_success_url(self):
        return '/poll/'+str(self.kwargs['pid'])+'/'
    # 表單驗證，在此填上選項所屬的投票主題 id
    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['pid']
        return super().form_valid(form)

        ## 修改投票選項
class OptionUpdate(UpdateView):
    model = Option
    fields = ['title']
    template_name = 'general_form.html'
    # 修改成功後返回其所屬投票主題檢視頁面
    def get_success_url(self):
        return '/poll/'+str(self.object.poll_id)+'/'

        ## 刪除投票選項
class OptionDelete(DeleteView):
    model = Option
    template_name = 'confirm_delete.html'
    # 刪除成功後返回其所屬投票主題檢視頁面
    def get_success_url(self):
        return reverse('poll_view', kwargs={'pk': self.object.poll_id})