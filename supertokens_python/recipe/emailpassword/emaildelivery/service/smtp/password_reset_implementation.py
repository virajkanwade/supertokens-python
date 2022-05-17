# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from os import path
from string import Template

from supertokens_python.ingredients.emaildelivery.service.smtp import \
    GetContentResult
from supertokens_python.recipe.emailpassword.types import \
    TypeEmailPasswordPasswordResetEmailDeliveryInput
from supertokens_python.supertokens import Supertokens


def get_password_reset_email_content(email_input: TypeEmailPasswordPasswordResetEmailDeliveryInput) -> GetContentResult:
    supertokens = Supertokens.get_instance()
    app_name = supertokens.app_info.app_name
    body = get_password_reset_email_html(app_name, email_input.user.email, email_input.password_reset_link)
    content_result = GetContentResult(body, "Password reset instructions", email_input.user.email)
    return content_result


def get_password_reset_email_html(appName: str, email: str, resetLink: str):
    current_dir = path.dirname(__file__)
    template_path = path.join(current_dir, "password_reset_email.html")
    template = open(template_path, "r").read()

    return Template(template).substitute(appName=appName, email=email, resetLink=resetLink)