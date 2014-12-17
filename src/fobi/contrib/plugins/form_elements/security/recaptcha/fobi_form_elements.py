__title__ = 'fobi.contrib.plugins.form_elements.security.recaptcha.fobi_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('ReCaptchaInputPlugin',)

import logging

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

DJANGO_RECAPTCHA_INSTALLED = False
DJANGO_SIMPLE_CAPTCHA_INSTALLED = False

try:
    import pip
    installed_packages = pip.get_installed_distributions()
    for installed_package in installed_packages:
        if "django-simple-captcha" == str(installed_package.key):
            DJANGO_SIMPLE_CAPTCHA_INSTALLED = True
            logger.error(
                "You have installed  the `django-simple-captcha` in your "
                "environment. At the moment you can't have both "
                "`django-simple-captcha` and `django-recaptcha` installed "
                "alongside due to app name collision (captcha). Remove "
                "both packages using pip uninstall and reinstall the"
                "`django-recaptcha` if you want to make use of the "
                "`fobi.contrib.plugins.form_elements.security.recaptcha` "
                "package."
                )
        if "django-recaptcha" == str(installed_package.key):
            DJANGO_RECAPTCHA_INSTALLED = True

except ImportError:
    try:
        from captcha.fields import ReCaptchaField
        from captcha.widgets import ReCaptcha as ReCaptchaWidget
        DJANGO_RECAPTCHA_INSTALLED = True
    except ImportError as e:
        DJANGO_RECAPTCHA_INSTALLED = False
        logger.error(
            "{0}{1}".format(str(e), "; Likely you didn't yet install the"
                            "`django-simple-captcha` package. Note, that at "
                            "the moment you can't have both `django-recaptcha` "
                            "and `django-simple-captcha` installed alongside "
                            "due to app name collision (captcha).")
            )

from fobi.base import FormElementPlugin, form_element_plugin_registry, get_theme
from fobi.contrib.plugins.form_elements.security.recaptcha import UID
from fobi.contrib.plugins.form_elements.security.recaptcha.forms import (
    ReCaptchaInputForm
    )

theme = get_theme(request=None, as_instance=True)

class ReCaptchaInputPlugin(FormElementPlugin):
    """
    ReCaptcha field plugin.
    """
    uid = UID
    name = _("ReCaptcha")
    group = _("Security")
    form = ReCaptchaInputForm

    def get_form_field_instances(self):
        """
        Get form field instances.
        """
        widget_attrs = {
            'class': theme.form_element_html_class,
            #'placeholder': self.data.placeholder,
        }

        kwargs = {
            'label': self.data.label,
            'help_text': self.data.help_text,
            #'initial': self.data.initial,
            'required': self.data.required,
            'widget': ReCaptchaWidget(attrs=widget_attrs),
        }

        return [(self.data.name, ReCaptchaField, kwargs)]


# Register only if safe to use.
if DJANGO_RECAPTCHA_INSTALLED and not DJANGO_SIMPLE_CAPTCHA_INSTALLED:
    form_element_plugin_registry.register(ReCaptchaInputPlugin)
