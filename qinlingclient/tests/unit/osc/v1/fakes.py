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
import hashlib
import mock
import six
import uuid

from osc_lib.tests import utils

from qinlingclient.tests.unit import fakes


class FakeQinlingClient(object):

    def __init__(self, **kwargs):
        self.auth_token = kwargs['auth_token']
        self.auth_url = kwargs['auth_url']
        self.runtimes = mock.Mock()
        self.functions = mock.Mock()
        self.function_executions = mock.Mock()
        self.function_versions = mock.Mock()


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


class FakeFunction(object):
    """Fake one or more functions."""

    @staticmethod
    def get_fake_md5():
        content = uuid.uuid4().hex
        if not isinstance(content, six.binary_type):
            content = content.encode('utf-8')
        return hashlib.md5(content).hexdigest()

    @staticmethod
    def create_one_function(attrs=None):
        """Create a fake function.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :return:
            A FakeResource object, with id, name, etc.
        """

        attrs = attrs or {}
        # Set default attributes.
        function_attrs = {
            'id': str(uuid.uuid4()),
            'name': 'function-name-' + uuid.uuid4().hex,
            'description': 'function-description-' + uuid.uuid4().hex,
            'count': 0,
            'code': {'md5sum': FakeFunction.get_fake_md5(),
                     'source': 'package'},
            'runtime_id': str(uuid.uuid4()),
            'entry': 'main.main',
            'project_id': str(uuid.uuid4()),
            'created_at': '2018-07-26 09:00:00',
            'updated_at': '2018-07-26 09:00:30',
            'cpu': 100,
            'memory_size': 33554432,
        }

        # Overwrite default attributes.
        function_attrs.update(attrs)

        function = fakes.FakeResource(info=copy.deepcopy(function_attrs),
                                      loaded=True)

        return function

    @staticmethod
    def create_functions(attrs=None, count=2):
        """Create multiple fake functions.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :param int count:
            The number of functions to fake
        :return:
            A list of FakeResource objects faking the functions.
        """

        functions = []
        for i in range(count):
            functions.append(FakeFunction.create_one_function(attrs))

        return functions

    @staticmethod
    def get_functions(functions=None, count=2):
        """Get an iterable Mock object with a list of faked functions.

        If functions list is provided, then initialize the Mock object with the
        list. Otherwise create one.

        :param List functions:
            A list of FakeResource faking functions
        :param int count:
            The number of functions to fake
        :return:
            An iterable Mock object with side_effect set to a list of faked
            functions.
        """

        if functions is None:
            functions = FakeFunction.create_functions(count=count)

        return mock.Mock(side_effect=functions)


class FakeExecution(object):
    """Fake one or more function executions."""

    @staticmethod
    def create_one_execution(attrs=None):
        """Create a fake function execution.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :return:
            A FakeResource object, with id, function_id, etc.
        """

        attrs = attrs or {}
        # Set default attributes.
        execution_attrs = {
            'id': str(uuid.uuid4()),
            'function_id': str(uuid.uuid4()),
            'function_version': 0,
            'description': 'execution-description-' + uuid.uuid4().hex,
            'input': '{"FAKE_INPUT_KEY": "FAKE_INPUT_VALUE"}',
            'result': '{"duration": 1.234, "output": "FAKE_OUTPUT"}',
            'status': 'success',
            'sync': True,
            'project_id': str(uuid.uuid4()),
            'created_at': '2018-07-26 09:00:00',
            'updated_at': '2018-07-26 09:00:30',
        }

        # Overwrite default attributes.
        execution_attrs.update(attrs)

        execution = fakes.FakeResource(info=copy.deepcopy(execution_attrs),
                                       loaded=True)

        return execution

    @staticmethod
    def create_executions(attrs=None, count=2):
        """Create multiple fake function executions.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :param int count:
            The number of function executions to fake
        :return:
            A list of FakeResource objects faking the function executions.
        """

        executions = []
        for i in range(count):
            executions.append(FakeExecution.create_one_execution(attrs))

        return executions

    @staticmethod
    def get_executions(executions=None, count=2):
        """Get an iterable Mock object with a list of faked executions.

        If function executions list is provided, then initialize the Mock
        object with the list. Otherwise create one.

        :param List executions:
            A list of FakeResource faking function executions
        :param int count:
            The number of function executions to fake
        :return:
            An iterable Mock object with side_effect set to a list of faked
            function executions.
        """

        if executions is None:
            executions = FakeExecution.create_executions(count=count)

        return mock.Mock(side_effect=executions)


class FakeFunctionVersion(object):
    """Fake one or more function versions."""

    @staticmethod
    def create_one_function_version(attrs=None):
        """Create a fake function version.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :return:
            A FakeResource object, with id, function_id, etc.
        """

        attrs = attrs or {}
        # Set default attributes.
        function_version_attrs = {
            'id': str(uuid.uuid4()),
            'function_id': str(uuid.uuid4()),
            'description': 'function-version-description-' + uuid.uuid4().hex,
            'version_number': 1,
            'count': 0,
            'project_id': str(uuid.uuid4()),
            'created_at': '2018-07-26 09:00:00',
            'updated_at': '2018-07-26 09:00:30',
        }

        # Overwrite default attributes.
        function_version_attrs.update(attrs)

        function_version = fakes.FakeResource(
            info=copy.deepcopy(function_version_attrs),
            loaded=True)

        return function_version

    @staticmethod
    def create_function_versions(attrs=None, count=2):
        """Create multiple fake function versions.

        :param Dictionary attrs:
            A dictionary with all atrributes
        :param int count:
            The number of function versions to fake
        :return:
            A list of FakeResource objects faking the function versions.
        """

        function_versions = []
        for i in range(count):
            function_versions.append(
                FakeFunctionVersion.create_one_function_version(attrs)
            )

        return function_versions

    @staticmethod
    def get_function_versions(function_versions=None, count=2):
        """Get an iterable Mock object with a list of faked function versions.

        If function versions list is provided, then initialize the Mock
        object with the list. Otherwise create one.

        :param List function_versions:
            A list of FakeResource faking function versions
        :param int count:
            The number of function versions to fake
        :return:
            An iterable Mock object with side_effect set to a list of faked
            function versions.
        """

        if function_versions is None:
            function_versions = FakeFunctionVersion.create_function_versions(
                count=count
            )

        return mock.Mock(side_effect=function_versions)
