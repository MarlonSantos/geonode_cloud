#########################################################################
#
# Copyright (C) 2024 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import os
from unittest.mock import MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
from geonode.upload.handlers.netcdf.exceptions import InvalidNetCDFException


class TestNetCDFFileHandler(TestCase):
    databases = ("default",)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.handler = NetCDFFileHandler()
        cls.valid_nc_files = {
            "base_file": "test_data.nc",
            "action": "upload",
        }
        cls.valid_netcdf_files = {
            "base_file": "test_data.netcdf",
            "action": "upload",
        }
        cls.invalid_files = {
            "base_file": "test_data.tif", 
            "action": "upload",
        }

    def test_supported_file_extension_config(self):
        """Test if supported file extension config is properly defined"""
        config = self.handler.supported_file_extension_config
        
        self.assertEqual(config["id"], "netcdf")
        self.assertEqual(config["type"], "raster")
        self.assertIn("upload", config["actions"])
        
        # Check if both .nc and .netcdf are supported
        extensions = []
        for format_info in config["formats"]:
            extensions.extend(format_info["required_ext"])
        
        self.assertIn("nc", extensions)
        self.assertIn("netcdf", extensions)

    def test_can_handle_nc_file(self):
        """Test if handler can handle .nc files"""
        result = NetCDFFileHandler.can_handle(self.valid_nc_files)
        self.assertTrue(result)

    def test_can_handle_netcdf_file(self):
        """Test if handler can handle .netcdf files"""
        result = NetCDFFileHandler.can_handle(self.valid_netcdf_files)
        self.assertTrue(result)

    def test_cannot_handle_invalid_file(self):
        """Test if handler correctly rejects non-NetCDF files"""
        result = NetCDFFileHandler.can_handle(self.invalid_files)
        self.assertFalse(result)

    def test_is_valid_with_missing_base_file(self):
        """Test validation with missing base file"""
        user = get_user_model().objects.create_user(username="testuser")
        files = {}
        
        with self.assertRaises(InvalidNetCDFException) as context:
            NetCDFFileHandler.is_valid(files, user)
        
        self.assertIn("base file is not provided", str(context.exception))

    def test_is_valid_with_invalid_filename(self):
        """Test validation with filename containing multiple dots"""
        user = get_user_model().objects.create_user(username="testuser")
        files = {"base_file": "test.data.nc"}
        
        with self.assertRaises(InvalidNetCDFException) as context:
            NetCDFFileHandler.is_valid(files, user)
        
        self.assertIn("additional dots", str(context.exception))

    def test_tasks_definition(self):
        """Test if TASKS are properly defined"""
        tasks = NetCDFFileHandler.TASKS
        
        # Check required task types
        self.assertIn("upload", tasks)
        self.assertIn("copy", tasks)
        self.assertIn("rollback", tasks)
        self.assertIn("replace", tasks)
        
        # Check that each task has required steps
        for action, steps in tasks.items():
            self.assertIsInstance(steps, tuple)
            self.assertGreater(len(steps), 0)
