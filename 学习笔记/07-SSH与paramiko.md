# 07 SSH 与 paramiko（服务器管理系统项目）

> 项目：F:\Server-manager 接口模块（PyCharm 项目在 D:\python\Lib\site-packages\QT_Project）
> 用途：给队友的 Qt 界面提供服务器管理接口，我只负责接口模块

## 第 1 课：SSH 原理与 paramiko（2026-10-16 完成 ✅）

**SSH 是什么**
- 加密的远程管理协议，替代明文传输的 telnet
- 握手阶段用非对称加密验证服务器身份+协商会话密钥，之后对称加密传输
- 服务器上 sshd 守护进程监听 22 端口
- 长连接：连上后通道保持，可反复执行命令（对比 API 的无状态请求）

**paramiko 四件套（顺序不能乱）**
1. `paramiko.SSHClient()` 创建连接管家
2. `set_missing_host_key_policy(paramiko.AutoAddPolicy())` 信任策略（不写连不上）
3. `connect(hostname=, port=, username=, password=)` 建立加密连接
4. `exec_command(cmd)` 执行命令，返回 stdin/stdout/stderr 三个管道

**踩过的坑**
- `stdout.read()` 返回 bytes，要 `.decode("utf-8")` 才能看；Windows GBK 控制台乱码是显示层问题，两层分开
- host key：paramiko 默认拒绝没见过的服务器（防中间人），AutoAddPolicy=练手用，真实工程要预登记 known_hosts
- **包是装在"解释器"里的，不是装在电脑里的**：PyCharm 项目的 venv 和命令行 python 各有一套包。给项目装包一律在 PyCharm 底部 Terminal 里 pip install（自动激活 venv）
- ping 通（ICMP）≠ SSH 通（TCP 22 端口），防火墙可以只放行其中一个
- 密码用 input() 运行时输入，不写死在代码里（git 安全课：进过历史=当已泄露）

**try/except 的意义**
- 出错时"体面地"告诉用户，而不是崩溃给堆栈看
- 故意输错密码对比体验：加 try/except 前后，报错从一屏英文堆栈变成一行提示

## 第 2 课：面向对象（进行中）

- 类 = 模板，对象 = 按模板造出来的实例；`SSHClient()`、`OpenAI(...)` 都是实例化
- self = 点号左边的那个对象
- 类解决"状态"问题：配置+连接状态跟着对象走，多台服务器互不干扰（对比全局变量的串台风险）
- 懒连接：__init__ 只存配置不连接；创建对象不该有副作用（手机存号码≠已拨号）
- 属性（is_connected）查状态，方法（connect/disconnect）做动作
- 自定义异常 ServerApiError：继承 Exception，super().__init__(message) 调用父类构造，不然 str(e) 是空的
- 异常转换：except Exception as e: raise ServerApiError(str(e))，把底层库的英文错误包成自己的异常

## 下一课（第 3 课）：exec_command 核心接口
