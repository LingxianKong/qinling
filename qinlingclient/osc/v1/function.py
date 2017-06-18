# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Qinling v1 function action implementation"""

from qinlingclient.osc.v1 import base


class List(base.QinlingLister):
    """List available runtimes."""

    def _get_resources(self, parsed_args):
        client = self.app.client_manager.function_engine

        return client.functions.list(**base.get_filters(parsed_args))

    def _list_columns(self):
        return ('id', 'name', 'count', 'code', 'runtime_id', 'entry',
                'created_at', 'updated_at')
