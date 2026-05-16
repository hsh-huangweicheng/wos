import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Switch, message, Popconfirm, Space, Tag } from 'antd'
import { PlusOutlined, DeleteOutlined, EditOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons'
import { db } from '../db'
import { Institution } from '../types'

function InstitutionConfig() {
  const [institutions, setInstitutions] = useState<Institution[]>([])
  const [modalVisible, setModalVisible] = useState(false)
  const [editingInst, setEditingInst] = useState<Institution | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    loadInstitutions()
  }, [])

  const loadInstitutions = async () => {
    const insts = await db.institutions.toArray()
    setInstitutions(insts)
  }

  const handleAdd = () => {
    setEditingInst(null)
    form.resetFields()
    form.setFieldsValue({ regex: false })
    setModalVisible(true)
  }

  const handleEdit = (record: Institution) => {
    setEditingInst(record)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = async (id: number) => {
    await db.institutions.delete(id)
    message.success('删除成功')
    loadInstitutions()
  }

  const handleSubmit = async (values: any) => {
    try {
      const instData: Institution = {
        nameCn: values.nameCn,
        nameEn: values.nameEn,
        regex: values.regex || false
      }

      // Validate regex if enabled
      if (instData.regex) {
        try {
          new RegExp(instData.nameEn)
        } catch (e) {
          message.error('无效的正则表达式')
          return
        }
      }

      if (editingInst?.id) {
        await db.institutions.update(editingInst.id, instData)
        message.success('更新成功')
      } else {
        await db.institutions.add(instData)
        message.success('添加成功')
      }

      setModalVisible(false)
      form.resetFields()
      loadInstitutions()
    } catch (error) {
      message.error('操作失败')
      console.error(error)
    }
  }

  const handleClearAll = async () => {
    await db.institutions.clear()
    message.success('已清空所有机构配置')
    loadInstitutions()
  }

  const handleTestRegex = async () => {
    const values = await form.getFieldsValue(['nameEn', 'regex'])
    if (!values.regex) {
      message.info('请先启用正则表达式模式')
      return
    }

    try {
      new RegExp(values.nameEn)
      message.success('正则表达式有效')
    } catch (e) {
      message.error('正则表达式无效: ' + (e as Error).message)
    }
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '中文名', dataIndex: 'nameCn', key: 'nameCn' },
    { title: '英文名/正则', dataIndex: 'nameEn', key: 'nameEn', ellipsis: true },
    {
      title: '正则',
      dataIndex: 'regex',
      key: 'regex',
      width: 80,
      render: (regex: boolean) => (
        regex ?
          <Tag color="green"><CheckCircleOutlined /> 是</Tag> :
          <Tag><CloseCircleOutlined /> 否</Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Institution) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>编辑</Button>
          <Popconfirm title="确认删除?" onConfirm={() => handleDelete(record.id!)}>
            <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加机构
          </Button>
          <Popconfirm title="确认清空所有机构配置?" onConfirm={handleClearAll}>
            <Button danger>清空全部</Button>
          </Popconfirm>
        </Space>
        <div style={{ marginTop: 16, color: '#666' }}>
          <p>说明：</p>
          <ul>
            <li>中文名：匹配后显示的中文机构名</li>
            <li>英文名/正则：用于匹配的英文关键词，支持正则表达式</li>
            <li>正则：启用后英文名将作为正则表达式进行匹配</li>
          </ul>
        </div>
      </div>

      <Table
        dataSource={institutions}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 20 }}
      />

      <Modal
        title={editingInst ? '编辑机构' : '添加机构'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="nameCn" label="中文名" rules={[{ required: true }]}>
            <Input placeholder="例如：清华大学" />
          </Form.Item>
          <Form.Item name="nameEn" label="英文名/正则" rules={[{ required: true }]}>
            <Input placeholder="例如：Tsinghua University 或 ^Tsinghua.*University$" />
          </Form.Item>
          <Form.Item name="regex" label="正则表达式" valuePropName="checked">
            <Switch checkedChildren="是" unCheckedChildren="否" />
          </Form.Item>
          <Button size="small" onClick={handleTestRegex}>测试正则</Button>
        </Form>
      </Modal>
    </div>
  )
}

export default InstitutionConfig
