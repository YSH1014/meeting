'''
用于model和form的相互转换，以应对model和form多变的需求
'''
from flask_wtf import FlaskForm
from abc import abstractclassmethod, abstractmethod


def diff_list(list1,list2):
    return [item for item in list1 if item not in list2]


class ModelFormRender:
    def __init__(self,model,form,ignore=[]):
        '''
        需保证model与form属性对应，一般model成员更多，所以以form为准
        :param model: 传入model的类，而不是对象
        :param form: 传入form的类，而不是对象
        :param ignore: 忽略的字段
        '''

        #首先存储类型信息
        self.model_type = model
        self.form_type = form

        flask_form_attr = dir(FlaskForm)
        form_attrs =  diff_list(dir(form),flask_form_attr)
        self.attrs = diff_list(form_attrs,ignore)
        self.attrs.remove("submit")   #submit当然不需要

    def m2f(self,model,form):
        '''
        用model 更新form
        :param model: model对象
        :param form: form对象
        :return:
        '''
        for attr in self.attrs:
            if hasattr(form,attr):
                value = getattr(model,attr)
                input_control = getattr(form,attr)
                input_control.data = value
            else:
                pass
        # 最后，修复特殊的
        self.fix_m2f(model,form)

    def f2m(self,model,form):
        '''
        用输入的form 更新model
        :param model:
        :param form:
        :return:
        '''
        for attr in self.attrs:
            if hasattr(model,attr):
                value=  getattr(form,attr).data
                setattr(model,attr,value)
            else:
                pass

        #最后修复特殊的
        self.fix_f2m(model,form)

    @abstractmethod
    def fix_m2f(self,model,form):
        pass

    @abstractmethod
    def fix_f2m(self,model,form):
        pass
