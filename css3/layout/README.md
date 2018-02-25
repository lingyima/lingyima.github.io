# cssrem 配置
- Sublime Text -> Preferences -> Browse Packages
- cssrem 文件夹放在上一步打开的目录中，重启sublime text即可生效

## 修改默认配置
- 打开cssrem 文件夹下的 cssrem.sublime-settings 文件进行修改
`{
    "px_to_rem": 40, //px转rem的单位比例，默认为40
    "max_rem_fraction_length": 6, //px转rem的小数部分的最大长度。默认为6。
    "available_file_types": [".css", ".less", ".sass",".html"]
    //启用此插件的文件类型。默认为：[".css", ".less", ".sass"]
}`
