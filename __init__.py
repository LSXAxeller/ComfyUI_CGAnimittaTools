# 导入所有节点类
from .PromptNegative_Selector import PromptNegativeSelector
from .List_Extractor import ExtractFromListNode
from .List_Subfolders import ListSubfoldersNode
from .BlackBorderCrop_node import BlackBorderCrop
from .Text_Reader import TxtReaderNode
from .DesaturateNode import ColorToGrayscale
from .FrameExtractionNode import FrameSelector
from .Blender_Bridge import BlenderBridgeNode

# 注册节点类，使用唯一的键标识每个节点
NODE_CLASS_MAPPINGS = {
    "CGA_NegativeSelector": PromptNegativeSelector,
    "CGA_ExtractFromList": ExtractFromListNode,
    "CGA_ListSubfolders": ListSubfoldersNode,
    "CGA_BlackBorderCrop": BlackBorderCrop,
    "CGA_TxtReaderNode": TxtReaderNode,
    "CGA_ColorToGrayscale": ColorToGrayscale,
    "CGA_FrameExtraction🎞️ ": FrameSelector,
    "CGA_BlenderBridge ": BlenderBridgeNode,

}
