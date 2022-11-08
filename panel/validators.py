from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext as _
def image_dimension_validator(width=None,height=None):
    def validator(image):
        error=False
        if width is not None and image.width < width:
            error=True
        if height is not None and image.height < height:
            error=True
        if error:
            raise ValidationError([f'Size should be atleast {width} x {height} pixels.'])
    return validator

class NumberValidator(object):
    def __init__(self,min_length=0):
        self.min_length=min_length
        
    def validate(self,password1,user=None):
        if not len(re.findall('\d',password1)) >=  self.min_length:
            raise ValidationError(_("The password must contain atleast %(min_length)d digit(s),0-9."),code="password_no_number",params={'min_length':self.min_length},)
    def get_help_text(self):
        return _('Your password must contain atleast  %(min_length)d digit, 0-9.' % {'min_length':self.min_length})

class UpperCaseValidator(object):
    def validate(self,password1,user=None):
        if not re.findall('[A-Z]',password1):
            raise ValidationError(_("The password must contain atleast 1 uppercase letter ,A-Z."),code="password_no_upper")
    def get_help_text(self):
        return _('Your password must contain atleast 1 uppercase letter, A-Z.')

class LowerCaseValidator(object):
    def validate(self,password1,user=None):
        if not re.findall('[a-z]',password1):
            raise ValidationError(_("The password must contain atleast 1 lowercase letter ,a-z."),code="password_no_lower")
    def get_help_text(self):
        return _('Your password must contain atleast 1 lowercase letter, a-z.')