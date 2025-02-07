# -*- coding: utf-8 -*-
"""
scan_conf - v1 serializers
"""
import logging

# 第三方
from rest_framework import serializers

# 项目内
from apps.scan_conf import models

logger = logging.getLogger(__name__)


class CheckToolNameSimpleSerializer(serializers.ModelSerializer):
    """工具名称简单序列化
    """
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, checktool):
        """获取工具展示名称
        """
        if checktool.show_display_name:
            return checktool.display_name
        return checktool.virtual_name

    class Meta:
        model = models.CheckTool
        fields = ["id", "name", "display_name"]
