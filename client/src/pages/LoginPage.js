import React, { useState } from 'react';
import withRouter from './withRouter';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Input, Button } from '@nextui-org/react';

const Login = () => {
    const navigate = useNavigate(); // 创建history对象
    const url = 'https://39808a7d.r19.cpolar.top'
    // 用户名和筹码量
    const [username, setUsername] = useState('');
    const [chips, setChips] = useState('');

    // 处理输入字段变化的函数
    const handleInputChange = (setter) => (e) => setter(e.target.value);

    // 处理登录逻辑的函数
    const handleSubmit = (e) => {
        e.preventDefault(); // 阻止表单默认提交行为
        // 在这里实现实际的登录验证逻辑

        console.log('登录信息', { url, username, chips });
        var seat = axios.post(url + '/l', {
            'name': username,
            'chips': chips
        }).then((res)=> {
            seat = res.data
            navigate('/table', {state: {seat, url}}); // 假设牌桌页面的路由是'/table'
        })
    };

    return (
        <div style={{ maxWidth: '300px', margin: '0 auto', padding: '20px' }}>
            <h2>登录</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <label htmlFor="username">用户名</label>
                    <Input
                        type="text"
                        id="username"
                        value={username}
                        onChange={handleInputChange(setUsername)}
                        style={{ display: 'block', width: '100%', marginTop: '5px' }}
                    />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label htmlFor="chips">筹码量</label>
                    <Input
                        type="number"
                        id="chips"
                        value={chips}
                        onChange={handleInputChange(setChips)}
                        style={{ display: 'block', width: '100%', marginTop: '5px' }}
                    />
                </div>
                <Button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                    登录
                </Button>
            </form>
        </div>
    );
};

export default withRouter(Login);
