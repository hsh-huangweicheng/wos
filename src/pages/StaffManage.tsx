import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, message, Upload, Popconfirm, Space, Tag } from 'antd'
import { PlusOutlined, UploadOutlined, DeleteOutlined, ExportOutlined } from '@ant-design/icons'
import Papa from 'papaparse'
import * as XLSX from 'xlsx'
import { db } from '../db'
import { Staff } from '../types'
import { generatePinyinVariants } from '../utils/pinyinMatcher'

function StaffManage() {
  const [staffList, setStaffList] = useState<Staff[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingStaff, setEditingStaff] = useState<Staff | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    loadStaff()
  }, [])

  const loadStaff = async () => {
    const staff = await db.staff.toArray()
    setStaffList(staff)
  }

  const handleAdd = () => {
    setEditingStaff(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (record: Staff) => {
    setEditingStaff(record)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = async (id: number) => {
    await db.staff.delete(id)
    message.success('删除成功')
    loadStaff()
  }

  const handleSubmit = async (values: any) => {
    try {
      const staffData: Staff = {
        department: values.department,
        name: values.name,
        position: values.position,
        pinyinVariants: generatePinyinVariants(values.name)
      }

      if (editingStaff?.id) {
        await db.staff.update(editingStaff.id, {
          department: staffData.department,
          name: staffData.name,
          position: staffData.position,
          pinyinVariants: staffData.pinyinVariants
        })
        message.success('更新成功')
      } else {
        await db.staff.add(staffData)
        message.success('添加成功')
      }

      setModalVisible(false)
      form.resetFields()
      loadStaff()
    } catch (error) {
      message.error('操作失败')
      console.error(error)
    }
  }

  const handleCSVUpload = async (file: File) => {
    setLoading(true)
    try {
      const content = await file.text()
      const result = Papa.parse(content, { header: true, skipEmptyLines: true })

      const staffData: Staff[] = result.data.map((row: any) => ({
        department: row['部门'] || row['department'] || '',
        name: row['姓名'] || row['name'] || '',
        position: row['职务'] || row['position'] || '',
        pinyinVariants: []
      }))

      // Generate pinyin variants
      for (const staff of staffData) {
        staff.pinyinVariants = generatePinyinVariants(staff.name)
      }

      // Deduplicate
      const existing = await db.staff.toArray()
      const existingKeys = new Set(existing.map(s => `${s.name}_${s.department}`))
      const newStaff = staffData.filter(s => !existingKeys.has(`${s.name}_${s.department}`))

      if (newStaff.length > 0) {
        await db.staff.bulkAdd(newStaff)
        message.success(`成功导入 ${newStaff.length} 条新员工数据`)
      } else {
        message.info('没有新的员工数据需要导入')
      }

      loadStaff()
    } catch (error) {
      message.error('CSV 解析失败')
      console.error(error)
    } finally {
      setLoading(false)
    }
    return false
  }

  const handleExport = () => {
    const exportData = staffList.map(s => ({
      '部门': s.department,
      '姓名': s.name,
      '职务': s.position,
      '拼音变体': s.pinyinVariants?.join(', ') || ''
    }))

    const ws = XLSX.utils.json_to_sheet(exportData)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '员工数据')
    XLSX.writeFile(wb, 'staff_export.xlsx')
    message.success('导出成功')
  }

  const handleClearAll = async () => {
    await db.staff.clear()
    message.success('已清空所有员工数据')
    loadStaff()
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '部门', dataIndex: 'department', key: 'department' },
    { title: '姓名', dataIndex: 'name', key: 'name' },
    { title: '职务', dataIndex: 'position', key: 'position' },
    {
      title: '拼音变体',
      dataIndex: 'pinyinVariants',
      key: 'pinyinVariants',
      render: (variants: string[]) => (
        <Space size={4} wrap>
          {variants?.slice(0, 3).map((v, i) => (
            <Tag key={i} color="blue">{v}</Tag>
          ))}
        </Space>
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Staff) => (
        <Space>
          <Button size="small" onClick={() => handleEdit(record)}>编辑</Button>
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
            添加员工
          </Button>
          <Upload beforeUpload={handleCSVUpload} showUploadList={false}>
            <Button icon={<UploadOutlined />} loading={loading}>
              导入 CSV
            </Button>
          </Upload>
          <Button icon={<ExportOutlined />} onClick={handleExport}>
            导出 Excel
          </Button>
          <Popconfirm title="确认清空所有员工数据?" onConfirm={handleClearAll}>
            <Button danger>清空全部</Button>
          </Popconfirm>
        </Space>
      </div>

      <Table
        dataSource={staffList}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 20 }}
      />

      <Modal
        title={editingStaff ? '编辑员工' : '添加员工'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="department" label="部门" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="position" label="职务">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default StaffManage
