# AstrBot LLM Reply Delay

让 AstrBot 在 LLM 回复生成后、发送到消息平台前等待一段时间。

## 功能

- 仅延迟 LLM 回复。
- 不修改回复内容。
- 不影响普通命令回复、其他插件主动发送消息。
- 不需要第三方依赖。

## 配置

在 AstrBot WebUI 的插件配置中调整：

- `基础设置 / 启用`: 是否启用插件，默认启用。
- `基础设置 / 延迟模式`: 延迟模式。
  - `fixed`: 固定秒数。
  - `random`: 随机区间。
  - `length`: 按回复长度计算。
- `固定延迟 / 等待秒数`: 固定模式下等待秒数，默认 `2.0`。
- `随机延迟 / 最小秒数` 和 `随机延迟 / 最大秒数`: 随机模式区间，默认 `1.0` 到 `5.0`。
- `按长度延迟 / 基础秒数`、`按长度延迟 / 每字秒数`、`按长度延迟 / 最大秒数`: 长度模式参数，默认 `0.5 + 回复字数 * 0.03`，最多 `10.0` 秒。

负数会按 `0` 处理；随机模式中最小值大于最大值时会自动交换。

## 安装

将插件目录放到 AstrBot 的插件目录：

```text
data/plugins/astrbot_plugin_llm_reply_delay
```

桌面版通常位于：

```text
C:\Users\<你的用户名>\.astrbot\data\plugins\astrbot_plugin_llm_reply_delay
```

然后在 AstrBot WebUI 的插件管理页重载或重启 AstrBot。
