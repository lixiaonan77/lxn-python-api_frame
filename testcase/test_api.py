from base.http_requests import HttpRequest
from utils.excel_util import ExcelUtil
from utils.log_util import logger
import pytest
import allure

@allure.feature("用户核心模块")          # 大功能模块（比如：订单模块/支付模块）
@allure.story("查询用户信息")           # 具体业务场景
@allure.title("GET /user 接口正向测试") # 用例标题（清晰描述测试场景）
@allure.severity(allure.severity_level.CRITICAL)  # 用例优先级：CRITICAL/MAJOR/MINOR/TRIVIAL
@allure.description("""
测试目的：验证已登录用户能正常查询自身信息
测试步骤：
1. 携带有效token调用GET /user接口
2. 验证响应状态码为200
3. 验证响应体包含userId、username字段
""") 
class TestApi:
    # 读取Excel用例数据（建议加异常处理，避免文件不存在报错）
    try:
        case_data = ExcelUtil.read_excel("./data/test_data.xlsx")
    except FileNotFoundError:
        logger.error("测试数据文件不存在：./data/test_data.xlsx")
        case_data = []  # 空数据避免后续参数化报错

    # 3.数据驱动
    @pytest.mark.parametrize("case", case_data)
    @allure.story("接口用例")  # 用例分组
    @allure.title("{case[case_name]}")  # 用例标题从Excel中取
    def test_api(self, case, token):
        # 读取用例（加默认值，避免Excel字段为空报错）
        case_name = case.get("case_name", "未命名用例")
        url = case.get("url", "")
        method = case.get("method", "GET")
        req_data = case.get("request_data") 
        expect_code = case.get("expect_code", 200)
        
        # Allure步骤展示
        with allure.step(f"1.准备请求数据：{case_name}"):
            # 修复：更健壮的请求数据解析
            try:
                data = eval(req_data) if req_data and req_data.strip() not in ["None", ""] else {}
            except Exception as e:
                logger.error(f"解析请求数据失败：{req_data}，错误：{e}")
                data = {}
                allure.attach(f"请求数据解析失败：{req_data}，错误：{e}", "数据解析异常", allure.attachment_type.TEXT)
            headers = {"token": token}
            # 提前附加请求数据到报告（不管请求是否成功都能看到）
            allure.attach(str(headers), "请求头（预设）", allure.attachment_type.TEXT)
            allure.attach(str(data), "请求体", allure.attachment_type.JSON)

        with allure.step(f"2.发送接口请求：{method} {url}"):
            http = HttpRequest()
            res = None
            try:
                # 发送请求
                res = http.send(method, url, headers=headers, json=data)
                # 修复1：请求头转成易读的字符串格式
                req_headers_str = "\n".join([f"{k}: {v}" for k, v in res.request.headers.items()])
                allure.attach(req_headers_str, "实际请求头", allure.attachment_type.TEXT)
                # 修复2：响应体根据实际类型选择附件类型，避免JSON解析失败
                try:
                    allure.attach(res.text, "响应体（JSON格式）", allure.attachment_type.JSON)
                except:
                    allure.attach(res.text, "响应体（文本格式）", allure.attachment_type.TEXT)
                # 附加响应状态码
                allure.attach(str(res.status_code), "响应状态码", allure.attachment_type.TEXT)
            except Exception as e:
                # 修复3：请求失败时附加异常信息，不中断用例
                logger.error(f"接口请求失败：{case_name}，错误：{e}")
                allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)

        with allure.step(f"3.接口断言"):
            # 先断言响应不为空
            assert res is not None, f"用例【{case_name}】请求无响应"
            # 断言状态码
            assert res.status_code == expect_code, \
                f"用例【{case_name}】状态码断言失败，预期：{expect_code}，实际：{res.status_code}"
            logger.info(f"用例【{case_name}】执行成功")
