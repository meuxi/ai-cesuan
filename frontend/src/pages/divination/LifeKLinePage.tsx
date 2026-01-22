// 重定向到新的人生K线页面
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LifeKLinePage: React.FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // 重定向到新版本的人生K线页面
        navigate('/divination/life-kline', { replace: true });
    }, [navigate]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                <p className="text-muted-foreground">正在跳转到新版本...</p>
            </div>
        </div>
    );
};

export default LifeKLinePage;
