import os
import sys
from typing import Optional

import yaml

from one_dragon.utils.log_utils import log


def get_temp_config_path(file_path: str) -> str:
    """
    优先检查PyInstaller运行时的_MEIPASS目录下是否有对应的yml文件
    有则返回该路径，否则返回原路径
    """
    if hasattr(sys, '_MEIPASS'):
        mei_path = os.path.join(sys._MEIPASS, 'config', os.path.basename(file_path))
        if os.path.exists(mei_path):
            return mei_path
    return file_path


class YamlOperator:

    def __init__(self, file_path: Optional[str] = None):
        """
        yml文件的操作器
        :param file_path: yml文件的路径。不传入时认为是mock，用于测试。
        """

        self.file_path: str = get_temp_config_path(file_path) if file_path else None
        """yml文件的路径"""

        self.data: dict = {}
        """存放数据的地方"""

        self.__read_from_file()

    def __read_from_file(self) -> None:
        """
        从yml文件中读取数据
        :return:
        """
        if self.file_path is None:
            return
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
        except Exception:
            log.error(f'文件读取失败 将使用默认值 {self.file_path}', exc_info=True)
            return

        if self.data is None:
            self.data = {}

    def save(self):
        if self.file_path is None:
            return

        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.data, file, allow_unicode=True, sort_keys=False)

    def save_diy(self, text: str):
        """
        按自定义的文本格式
        :param text: 自定义的文本
        :return:
        """
        if self.file_path is None:
            return

        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(text)

    def get(self, prop: str, value=None):
        return self.data.get(prop, value)

    def update(self, key: str, value, save: bool = True):
        if self.data is None:
            self.data = {}
        if key in self.data and not isinstance(value, list) and self.data[key] == value:
            return
        self.data[key] = value
        if save:
            self.save()

    def delete(self):
        """
        删除配置文件
        :return:
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def is_file_exists(self) -> bool:
        """
        配置文件是否存在
        :return:
        """
        return os.path.exists(self.file_path)
