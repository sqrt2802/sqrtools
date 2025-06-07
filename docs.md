## docs.md

sqrtools 的接口调用指南。

在开发算号代码之前，建议先阅读[教程](https://namerena-help.pages.dev)的算号部分。

------

### 在代码中添加 sqrtools

下载的 pyc 文件可以作为 python 库文件使用。把它和你的代码放在同一个文件夹（也可以是 `sys.path` 中的任意目录）中，使用一个合适的文件名，并直接在你的代码中导入即可：

```python
import sqrtoolsfile as sqrtools    #导入名为 sqrtoolsfile.pyc 的文件
my_awesome_name=sqrtools.Name()    #创建一个新的空白名字
```

你可以通过 `sqrtools.SQRTOOLS_VERSION` 来查看 sqrtools 版本。

sqrtools 的主要功能是名为 `Name` 的 python 类。

### Name 类型属性

`Name` 中包含以下数值：

- `namebase`, `namebonus`, `nameprop`: 顾名思义。`nameprop` 从前到后分别为 \[HP, 攻, 防, 速, 敏, 魔, 抗, 智\] 数值。

- `nameskill` : 存储名字技能的 int 数组，由 16 个形如 (id, 熟练度) 的二元组组成。技能 id 与名称的对应关系如下：

id|0|1|2|3|4|5|6|7|8|9
:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:
技能|火球|冰冻|雷击|地裂|吸血|投毒|连击|会心|瘟疫|命轮
**id**|**10**|**11**|**12**|**13**|**14**|**15**|**16**|**17**|**18**|**19**
技能|狂暴|魅惑|加速|减速|诅咒|治愈|苏生|净化|铁壁|蓄力
**id**|**20**|**21**|**22**|**23**|**24**|**25**|**26**|**27**|**28**|**29**
技能|聚气|潜行|血祭|分身|幻术|防御|守护|反弹|护符|护盾
**id**|**30**|**31**|**32**|**33**|**34**|**35**|**36**|**37**|**38**|**39**
技能|反击|吞噬|亡灵|垂死|隐匿|(空技能)|(空技能)|(空技能)|(空技能)|(空技能)

### Name 类型方法

使用 `Name()` 可以创建一个新的空白名字。

`Name` 类型包含以下用于算号的函数方法：

- `load(namein:str)->bool` : 载入字符串并计算 `val` 和 `namebase`。若操作成功则返回 `True`，否则返回 `False`。

- `calcprops(usebonus:bool)->None` : 计算名字属性。当 `usebonus` 为 `True` 时将开启加成功能，否则只返回单号技能。

- `calcskill(self,usebonus:bool)->None` : 计算名字技能，参数同上。

计算完成后，你需要手动调用 Name 变量下相关的属性数组查看结果。

以下是一个计算名字数值属性的示例程序：

```python
import sqrtools
name=sqrtools.Name()
name.load('1')
name.calcprops()
print(name.nameprop)
```
