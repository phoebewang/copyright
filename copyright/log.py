import logging

logger = logging.getLogger('root')
FORMAT = "%(asctime)-15s %(filename)s:%(lineno)s %(funcName)s() %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

# copyright - Add or replace license boilerplate.
# Copyright (C) 2016 Remik Ziemlinski
# 
# copyright is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# copyright is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.