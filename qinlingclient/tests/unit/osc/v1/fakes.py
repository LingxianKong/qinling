# Copyright 2018 AWCloud Software Co., Ltd.
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

import copy
import mock
import uuid

from osc_lib.tests import utils

from qinlingclient.tests.unit import fakes


class FakeQinlingClient(object):

    def __init__(self, **kwargs):
        self.auth_token = kwargs['auth_token']
        self.auth_url = kwargs['auth_url']
        self.runtimes = mock.Mock()


class TestQinlingClient(utils.TestCommand):

    def setUp(self):
        super(TestQinlingClient, self).setUp()
        self.app.client_manager.function_engine = FakeQinlingClient(
            auth_token=fakes.AUTH_TOKEN,
            auth_url=fakes.AUTH_URL
        )


class FakeRuntime(object):
    """Fake one or more runtimes."""

    @staticmethod
    def create_one_runtime(attrs=None):
        """Create a fake runtime.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :return:
            A FakeResource object, with id, name, etc.
        """

        attrs = attrs or {}
        # Set default attributes.
        runtime_attrs = {
            'id': str(uuid.uuid4()),
            'name': 'runtime-name-' + uuid.uuid4().hex,
            'image': 'openstackqinling/python-runtime',
            'status': 'available',
            'description': 'runtime-description-' + uuid.uuid4().hex,
            'is_public': True,
            'trusted': True,
            'project_id': str(uuid.uuid4()),
            'created_at': '2018-07-26 09:00:00',
            'updated_at': '2018-07-26 09:00:30'
        }

        # Overwrite default attributes.
        runtime_attrs.update(attrs)

        runtime = fakes.FakeResource(info=copy.deepcopy(runtime_attrs),
                                     loaded=True)

        return runtime

    @staticmethod
    def create_runtimes(attrs=None, count=2):
        """Create multiple fake runtimes.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :param int count:
            The number of runtimes to fake
        :return:
            A list of FakeResource objects faking the runtimes.
        """

        runtimes = []
        for i in range(count):
            runtimes.append(FakeRuntime.create_one_runtime(attrs))

        return runtimes

    @staticmethod
    def get_runtimes(runtimes=None, count=2):
        """Get an iterable Mock object with a list of faked runtimes.

        If runtimes list is provided, then initialize the Mock object with the
        list. Otherwise create one.

        :param List runtimes:
            A list of FakeResource faking runtimes
        :param int count:
            The number of runtimes to fake
        :return:
            An iterable Mock object with side_effect set to a list of faked
            runtimes.
        """

        if runtimes is None:
            runtimes = FakeRuntime.create_runtimes(count=count)

        return mock.Mock(side_effect=runtimes)

    @staticmethod
    def create_one_runtime_pool(attrs=None):
        """Create a fake runtime pool.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :return:
            A FakeResource object, with name, capacity.
        """

        attrs = attrs or {}
        # Set default attributes.
        pool_attrs = {
            'name': 'runtime-id-' + uuid.uuid4().hex,
            'capacity': {'available': 5, 'total': 5}
        }

        # Overwrite default attributes.
        pool_attrs.update(attrs)

        runtime_pool = fakes.FakeResource(info=copy.deepcopy(pool_attrs),
                                          loaded=True)

        return runtime_pool
