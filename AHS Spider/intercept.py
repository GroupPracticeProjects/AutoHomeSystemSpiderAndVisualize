# -*- coding:utf-8 -*-
# Author: cq
# Time: 2020/11/22 15:19
# 
#
import re
from mitmproxy import ctx


def response(flow):
    """修改应答数据
    """
    # if 'GetModelConfig' in flow.request.url:
    # 汽车之家字符混淆（CSS :before 伪元素）破解
    ctx.log.info('*' * 120 + '\n Found {}.'.format(flow.request.url))
    m = re.compile(
        r'''function\s*(\$InsertRule\$)\s*\((\$\w+\$),\s*(\$\w+\$)''',
        re.IGNORECASE).search(flow.response.text)
    if m:
        # 提取函数名和参数
        function_name = m.groups()[0]
        param1 = m.groups()[1]
        param2 = m.groups()[2]
        ctx.log.info('Crack "CSS :before" in {}: "{}"'.format(function_name, flow.request.url))
        
        # 替换后的内容
        replacement = "function $InsertRule$ ($index$, $item$){" + "document.head.appendChild(document.createTextNode('[' + {} + ']->{{' + {} + '}};'));".format(
            param1, param2) + "console.log({} + '->' + {});".format(param1, param2)
        # replacement = "function $InsertRule$ ($index$, $item$){" + "console.log({} + '->' + {});".format(param1, param2)
        flow.response.text = flow.response.text.replace("function $InsertRule$ ($index$, $item$){", replacement)
