# coding=utf-8
# Date: 15/1/30
# Time: 22:57
# Email:fanjunwei003@163.com

__author__ = u'范俊伟'

template = '''
            <div class="form-group " input-group="{0}">

                <label for="{0}" class="col-sm-2 control-label">{1}<span class="required">*</span></label>

                <div class="col-sm-10 controls ">
                     <input data-toggle="tooltip" data-placement="top" style="max-width: 500px;" type="text"
                           class="form-control" id="{0}" name="{0}" placeholder="{1}" maxlength="" value="{{{{{0}}}}}"
                           input-check="required">

                    <div input-errors="{0}" class="text-danger"></div>
                </div>
            </div>
'''

items = [
    ('company', '领料单位'),
    ('lingliaoren', '领料人'),
]
for i in items:
    print template.format(*i)
