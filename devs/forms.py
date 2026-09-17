from django import forms

from .models import PortalMenu


# =====================================================
# Portal Menu Form
# =====================================================

class PortalMenuForm(forms.ModelForm):

    class Meta:

        model = PortalMenu

        fields = [
            "menu_name",
            "parent",
            "display_order",
            "has_page",
            "menu_url",
            "requires_permission",
            "is_active",
        ]

        widgets = {

            "menu_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter menu name"
                }
            ),

            "parent": forms.Select(
                attrs={
                    "class": "form-input"
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": 1
                }
            ),

            "has_page": forms.Select(
                choices=[
                    ("N", "No"),
                    ("Y", "Yes"),
                ],
                attrs={
                    "class": "form-input"
                }
            ),

            "menu_url": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "/example/"
                }
            ),

            "requires_permission": forms.Select(
                choices=[
                    ("N", "No"),
                    ("Y", "Yes"),
                ],
                attrs={
                    "class": "form-input"
                }
            ),

            "is_active": forms.Select(
                choices=[
                    ("Y", "Yes"),
                    ("N", "No"),
                ],
                attrs={
                    "class": "form-input"
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        has_page = cleaned_data.get("has_page")
        menu_url = cleaned_data.get("menu_url")

        if has_page == "Y" and not menu_url:

            self.add_error(
                "menu_url",
                "Page URL is required when this menu has a page."
            )

        if has_page == "N":

            cleaned_data["menu_url"] = ""

            cleaned_data["requires_permission"] = "N"

        if self.instance.pk:

            parent = cleaned_data.get("parent")

            if parent == self.instance:

                self.add_error(
                    "parent",
                    "A menu cannot be its own parent."
                )

        return cleaned_data