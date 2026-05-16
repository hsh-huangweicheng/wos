import { useState } from 'react'
import { Layout, Menu } from 'antd'
import Home from './pages/Home'
import StaffManage from './pages/StaffManage'
import InstitutionConfig from './pages/InstitutionConfig'

const { Header, Content } = Layout

function App() {
  const [currentPage, setCurrentPage] = useState('home')

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <Home />
      case 'staff':
        return <StaffManage />
      case 'institution':
        return <InstitutionConfig />
      default:
        return <Home />
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '40px' }}>
          WOS 匹配工具
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[currentPage]}
          onClick={(e) => setCurrentPage(e.key)}
          items={[
            { key: 'home', label: '数据处理' },
            { key: 'staff', label: '员工管理' },
            { key: 'institution', label: '机构配置' },
          ]}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '24px', background: '#fff' }}>
        {renderPage()}
      </Content>
    </Layout>
  )
}

export default App
