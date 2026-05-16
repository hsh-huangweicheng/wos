// WOS 记录类型
export interface WOSRecord {
  id: string
  pt: string           // 出版物类型
  ut: string           // BIOSIS 入藏号
  ti: string           // 文献标题
  so: string           // 来源出版物
  py: string           // 出版年
  au: string[]         // 作者列表
  af: string[]         // 作者全名列表
  c1: string           // 作者地址
  em: string           // 电子邮件
  di: string           // DOI
  tc: string           // 被引频次
  authors: AuthorInfo[]
}

// 作者信息
export interface AuthorInfo {
  name: string           // 英文名（格式：姓, 名）
  fullName: string       // 全名
  institution: string    // 机构英文名
  institutionCn: string  // 机构中文名（匹配后）
  matched: boolean       // 是否已匹配
}

// 员工类型
export interface Staff {
  id?: number
  department: string     // 现部门
  name: string           // 姓名
  position: string       // 单位职务
  pinyinVariants: string[]  // 拼音变体
  createdAt?: string
}

// 机构配置
export interface Institution {
  id?: number
  nameCn: string         // 中文名
  nameEn: string         // 英文名（支持正则）
  regex: boolean         // 是否为正则表达式
}

// 匹配结果
export interface MatchResult {
  id: string
  wosRecord: WOSRecord
  author: AuthorInfo
  staff?: Staff          // 匹配的员工
  institutionCn: string  // 机构中文名
  matchType: 'auto' | 'manual' | 'unmatched'
}

// 统计数据
export interface MatchStats {
  totalRecords: number
  totalAuthors: number
  matchedAuthors: number
  unmatchedAuthors: number
  matchedWithCnInstitution: number  // 有中文机构名且匹配成功的
}
