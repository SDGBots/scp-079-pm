# SCP-079-PM - Everyone can have their own Telegram private chat bot
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-PM.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pickle
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from threading import Lock
from typing import List, Dict, Set, Tuple, Union

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
backup: Union[str, bool] = ""
date_reset: str = ""
flood_ban: int = 0
flood_limit: int = 0
flood_time: int = 0
host_id: int = 0
host_name: str = ""
project_link: str = ""
project_name: str = ""
zh_cn: Union[str, bool] = ""

# [encrypt]
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    date_reset = config["custom"].get("date_reset", date_reset)
    flood_ban = int(config["custom"].get("flood_ban", flood_ban))
    flood_limit = int(config["custom"].get("flood_limit", flood_limit))
    flood_time = int(config["custom"].get("flood_time", flood_time))
    host_id = int(config["custom"].get("host_id", host_id))
    host_name = config["custom"].get("host_name", host_name)
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)
    # [encrypt]
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}")

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or backup not in {False, True}
        or date_reset in {"", "[DATA EXPUNGED]"}
        or flood_ban == 0
        or flood_limit == 0
        or flood_time == 0
        or host_id == 0
        or host_name in {"", "[DATA EXPUNGED]"}
        or zh_cn not in {False, True}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    "admin_group": (zh_cn and "群管理") or "Group Admin",
    "admin_project": (zh_cn and "项目管理员") or "Project Admin",
    # Basic
    "action": (zh_cn and "执行操作") or "Action",
    "colon": (zh_cn and "：") or ": ",
    "description": (zh_cn and "说明") or "Description",
    "disabled": (zh_cn and "禁用") or "Disabled",
    "enabled": (zh_cn and "启用") or "Enabled",
    "error": (zh_cn and "错误") or "Error",
    "reason": (zh_cn and "原因") or "Reason",
    "reset": (zh_cn and "重置数据") or "Reset Data",
    "rollback": (zh_cn and "数据回滚") or "Rollback",
    "status_failed": (zh_cn and "未执行") or "Failed",
    "type": (zh_cn and "类别") or "Type",
    "version": (zh_cn and "版本") or "Version",
    # Command
    "command_lack": (zh_cn and "命令参数缺失") or "Lack of Parameter",
    "command_para": (zh_cn and "命令参数有误") or "Incorrect Command Parameter",
    "command_type": (zh_cn and "命令类别有误") or "Incorrect Command Type",
    "command_usage": (zh_cn and "用法有误") or "Incorrect Usage",
    # Data
    "blacklist": (zh_cn and "黑名单") or "Blacklist",
    "message_id": (zh_cn and "消息 ID") or "Message ID",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Record
    "project": (zh_cn and "项目编号") or "Project",
    "project_origin": (zh_cn and "原始项目") or "Original Project",
    "status": (zh_cn and "状态") or "Status",
    "user_id": (zh_cn and "用户 ID") or "User ID",
    "level": (zh_cn and "操作等级") or "Level",
    "rule": (zh_cn and "规则") or "Rule",
    "message_type": (zh_cn and "消息类别") or "Message Type",
    "message_game": (zh_cn and "游戏标识") or "Game Short Name",
    "message_lang": (zh_cn and "消息语言") or "Message Language",
    "message_len": (zh_cn and "消息长度") or "Message Length",
    "message_freq": (zh_cn and "消息频率") or "Message Frequency",
    "user_score": (zh_cn and "用户得分") or "User Score",
    "user_bio": (zh_cn and "用户简介") or "User Bio",
    "user_name": (zh_cn and "用户昵称") or "User Name",
    "from_name": (zh_cn and "来源名称") or "Forward Name",
    "more": (zh_cn and "附加信息") or "Extra Info",
    # Special
    "chat_id": (zh_cn and "对话 ID") or "Chat ID",
    "reason_blacklist": (zh_cn and "该用户在黑名单中") or "The User is in the Blacklist",
    "reason_not_blocked": (zh_cn and "该用户不在黑名单中") or "The User is Not Blocked",
    "reason_stopped": (zh_cn and "对方已停用机器人") or "The User Stopped the Bot",
    "recall": (zh_cn and "撤回") or "Recall",
    "to_id": (zh_cn and "发送至 ID") or "Delivered to ID",
    # Status
    "status_cleared": (zh_cn and "已清空") or "Cleared",
    "status_delivered": (zh_cn and "已发送") or "Delivered",
    "status_edited": (zh_cn and "已编辑") or "Edited",
    "status_error": (zh_cn and "出现错误") or "Error Occurred",
    "status_recalled": (zh_cn and "已撤回") or "Recalled",
    "status_recalled_all": (zh_cn and "已撤回全部消息") or "Recalled All Messages",
    "status_recalled_all_host": (zh_cn and "已撤回由您发送的全部消息") or "Recalled All Messages from You",
    "status_recalled_none": (zh_cn and "没有可撤回的消息") or "Recalled No Messages",
    "status_resent": (zh_cn and "已重新发送并撤回旧消息") or "Resent and Deleted the Old Message",
    "status_unblocked": (zh_cn and "已解禁") or "Unblocked",
}

# Init

all_commands: List[str] = [
    "block",
    "clear",
    "direct",
    "leave",
    "mention",
    "now",
    "ping",
    "recall",
    "start",
    "status",
    "unblock",
    "version"
]

flood_ids: Dict[str, Union[Dict[int, int], set]] = {
    "users": set(),
    "counts": {}
}
# flood_ids = {
#     "users": {12345678},
#     "counts": {12345678: 0}
# }

locks: Dict[str, Lock] = {
    "message": Lock()
}

sender: str = "PM"

should_hide: bool = False

version: str = "0.4.3"

direct_chat: int = 0

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)

# Init ids variables

blacklist_ids: Set[int] = set()
# blacklist_ids = {12345678}

message_ids: Dict[int, Dict[str, Set[int]]] = {}
# message_ids = {
#     12345678: {
#         "guest": {123},
#         "host": {456}
#     }
# }

reply_ids: Dict[str, Dict[int, Tuple[int, int]]] = {
    "g2h": {},
    "h2g": {}
}
# reply_ids = {
#     "g2h": {
#         123: (124, 12345678)
#     },
#     "h2g": {
#         124: (123, 12345678)
#     }
# }

# Init data variables

status: str = ""

# Load data
file_list: List[str] = ["blacklist_ids", "message_ids", "reply_ids", "status"]
for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", 'rb') as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", 'wb') as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)
            with open(f"data/.{file}", 'rb') as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
