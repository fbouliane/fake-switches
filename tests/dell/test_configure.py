# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from flexmock import flexmock_teardown

from tests.dell import enable, configure, configuring_vlan, unconfigure_vlan, \
    ssh_protocol_factory, telnet_protocol_factory
from tests.util.protocol_util import with_protocol


class DellConfigureTest(unittest.TestCase):
    __test__ = False
    protocol_factory = None

    def setUp(self):
        self.protocol = self.protocol_factory()

    def tearDown(self):
        flexmock_teardown()

    @with_protocol
    def test_entering_configure_interface_mode(self, t):
        enable(t)
        configure(t)

        t.write("interface ethernet 1/g1")
        t.readln("")
        t.read("my_switch(config-if-1/g1)#")

        t.write("exit")
        t.readln("")
        t.read("my_switch(config)#")

        t.write("exit")
        t.readln("")
        t.read("my_switch#")

    @with_protocol
    def test_entering_vlan_database_mode(self, t):
        enable(t)
        configure(t)

        t.write("vlan database")
        t.readln("")
        t.read("my_switch(config-vlan)#")

        t.write("exit")
        t.readln("")
        t.read("my_switch(config)#")

        t.write("exit")
        t.readln("")
        t.read("my_switch#")

    @with_protocol
    def test_editing_vlan(self, t):
        enable(t)
        configure(t)

        t.write("interface vlan 1260")
        t.readln("VLAN ID not found.")
        t.readln("")

        t.read("my_switch(config)#")
        t.write("exit")
        t.readln("")
        t.read("my_switch#")

        configuring_vlan(t, 1260)

        configure(t)
        t.write("interface vlan 1260")
        t.readln("")
        t.read("my_switch(config-if-vlan1260)#")

        t.write("exit")
        t.readln("")
        t.read("my_switch(config)#")

        unconfigure_vlan(t, 1260)


class DellConfigureSshTest(DellConfigureTest):
    __test__ = True
    protocol_factory = ssh_protocol_factory 


class DellConfigureTelnetTest(DellConfigureTest):
    __test__ = True
    protocol_factory = telnet_protocol_factory
