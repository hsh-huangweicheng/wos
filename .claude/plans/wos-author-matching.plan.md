# WOS作者匹配工具 - 实施计划

## 项目结构
```
wos/
├── data/
│   ├── wos/                    # WOS文件输入目录
│   │   └── savedrecs.txt
│   ├── config/
│   │   ├── 员工.csv            # 员工配置
│   │   └── 机构.csv            # 机构配置
│   └── 结果.csv                # 输出结果
├── src/
│   ├── index.ts                # 入口文件
│   ├── parser/
│   │   ├── wosParser.ts        # WOS文件解析
│   │   └── csvParser.ts        # CSV解析
│   ├── matcher/
│   │   ├── preprocessor.ts     # 预处理
│   │   ├── institutionMatcher.ts  # 机构匹配
│   │   └── authorMatcher.ts   # 作者匹配
│   └── writer/
│       └── resultWriter.ts    # 结果输出
├── tests/                      # 单元测试
├── package.json
└── tsconfig.json
```

## 实现步骤

### Step 1: 项目初始化
- 初始化 npm + TypeScript
- 安装依赖（csv-parse, vitest等）

### Step 2: WOS解析器
- 解析 savedrecs.txt 格式
- 提取 AU, AF, UT, C1 字段

### Step 3: CSV解析器
- 加载员工配置
- 加载机构配置

### Step 4: 预处理模块
- 转小写
- 非字母数字→空格
- 连续空格合并
- 头尾空格去掉

### Step 5: 机构匹配
- 正则匹配（忽略大小写）
- 解析C1中的作者列表

### Step 6: 作者匹配
- 拼音全匹配
- 处理相同拼音（方括号）
- 确定第几作者

### Step 7: 结果输出
- 去重（UT+英文姓名）
- 输出CSV

### Step 8: 单元测试
- 覆盖率 >80%

## 验证
- 运行 `npm run build` 编译
- 运行 `npm test` 测试
- 手动测试 data/wos/savedrecs.txt
