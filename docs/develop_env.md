# 无网络迁移python环境

1. **代码库内容**：在有网络连接的电脑上，通过以下命令克隆GitHub代码库：

```bash
git clone https://github.com/SuuTTT/wuliu0603.git
```

2. **依赖**：该项目在`requirements.txt`文件中列出了Python的依赖包，你需要在有网络的电脑上安装这些依赖，并下载这些依赖的安装包（轮子文件）以供离线安装。对于Python，你可以使用pip来做：

```bash
pip download -r wuliu0603/requirements.txt -d ./my_dir
```

这个命令会下载所有在`requirements.txt`文件中列出的依赖包的轮子文件到`./my_dir`文件夹。

3. **文件传输**：在你克隆了代码库和下载了依赖包之后，将这些文件拷贝到USB驱动器，外置硬盘，或者其他任何可以携带的存储设备上。

4. **离线电脑设置**：将你的存储设备插入到你的离线电脑上，将代码库和依赖包的文件拷贝到合适的目录。

5. **安装依赖**：使用你之前下载的轮子文件来安装依赖。对于Python，你还可以使用pip：

```bash
pip install --no-index --find-links=./my_dir -r wuliu0603/requirements.txt
```
