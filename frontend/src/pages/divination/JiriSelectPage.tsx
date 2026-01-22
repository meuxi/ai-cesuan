import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { yijiList } from '@/utils/laohuangli'
import { ChevronLeft } from 'lucide-react'
import './laohuangli.css'

export default function JiriSelectPage() {
  const navigate = useNavigate()
  const [yijiType, setYijiType] = useState<1 | 2>(1) // 1: 宜, 2: 忌

  const handleToDetail = (name: string) => {
    navigate(`/divination/laohuangli/detail?name=${encodeURIComponent(name)}&type=${yijiType}`)
  }

  const handleBack = () => {
    navigate('/divination/laohuangli')
  }

  return (
    <div className="jiri-select-wrapper">
      {/* 导航栏 */}
      <div className="jiri-select-nav">
        <div className="jiri-nav-back" onClick={handleBack}>
          <ChevronLeft className="w-6 h-6" />
        </div>
        <div className="jiri-nav-center">
          <div className="jiri-type-switch">
            <div
              className={`jiri-type-item ${yijiType === 1 ? 'active-yi' : ''}`}
              onClick={() => setYijiType(1)}
            >
              宜
            </div>
            <div
              className={`jiri-type-item ${yijiType === 2 ? 'active-ji' : ''}`}
              onClick={() => setYijiType(2)}
            >
              忌
            </div>
          </div>
        </div>
        <div className="jiri-nav-right"></div>
      </div>

      {/* 分类列表 */}
      <div className="jiri-select-content">
        {yijiList.map((category, index) => (
          <div key={index} className="jiri-category-card">
            <div className="p-4">
              <div className={`jiri-category-title ${yijiType === 2 ? 'ji-title' : ''}`}>
                {category.type}
              </div>
              <div className="jiri-items-grid">
                {category.childrens.split(' ').map((item, idx) => (
                  <div
                    key={idx}
                    className={`jiri-item ${yijiType === 2 ? 'ji-item' : ''}`}
                    onClick={() => handleToDetail(item)}
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      <style>{`
        .jiri-select-wrapper {
          min-height: calc(100vh - 120px);
          padding-bottom: 20px;
        }

        .jiri-select-nav {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          background: hsl(var(--card));
          border-radius: 12px;
          margin-bottom: 16px;
          position: sticky;
          top: 0;
          z-index: 50;
        }

        .jiri-nav-back {
          cursor: pointer;
          padding: 4px;
          border-radius: 8px;
          transition: background 0.2s;
        }

        .jiri-nav-back:hover {
          background: hsl(var(--accent));
        }

        .jiri-nav-center {
          flex: 1;
          display: flex;
          justify-content: center;
        }

        .jiri-nav-right {
          width: 32px;
        }

        .jiri-type-switch {
          display: flex;
          border: 1px solid hsl(var(--jiri-yi));
          border-radius: 6px;
          overflow: hidden;
        }

        .jiri-type-item {
          padding: 6px 20px;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s;
          color: hsl(var(--foreground));
        }

        .jiri-type-item.active-yi {
          background: hsl(var(--jiri-yi));
          color: white;
        }

        .jiri-type-item.active-ji {
          background: hsl(var(--jiri-ji));
          color: white;
        }

        .jiri-select-content {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .jiri-category-card {
          overflow: hidden;
        }

        .jiri-category-title {
          font-size: 18px;
          font-weight: bold;
          color: hsl(var(--jiri-yi));
          margin-bottom: 12px;
          padding-left: 8px;
          border-left: 3px solid hsl(var(--jiri-yi));
        }

        .jiri-category-title.ji-title {
          color: hsl(var(--jiri-ji));
          border-left-color: hsl(var(--jiri-ji));
        }

        .jiri-items-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }

        .jiri-item {
          width: calc(33.333% - 8px);
          text-align: center;
          padding: 8px 4px;
          background: hsl(var(--jiri-yi-light));
          border: 1px solid hsl(var(--jiri-yi-light));
          color: hsl(var(--jiri-yi));
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
          font-size: 14px;
        }

        .jiri-item:hover {
          transform: scale(1.05);
          box-shadow: 0 2px 8px hsl(var(--jiri-yi) / 0.3);
        }

        .jiri-item.ji-item {
          background: hsl(var(--jiri-ji-light));
          border-color: hsl(var(--jiri-ji-light));
          color: hsl(var(--jiri-ji));
        }

        .jiri-item.ji-item:hover {
          box-shadow: 0 2px 8px hsl(var(--jiri-ji) / 0.3);
        }
      `}</style>
    </div>
  )
}
