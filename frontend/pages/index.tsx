
import React, { useEffect, useState } from 'react';
export default function Dashboard() {
    const [data, setData] = useState<any>(null);
    useEffect(() => {
        fetch('http://localhost:8000/api/v1/analyze')
            .then(res => res.json()).then(d => setData(d));
    }, []);
    return (
        <div style={{padding: '50px', backgroundColor: '#f0f2f5', minHeight: '100vh'}}>
            <h1>UMLFI Multi-Language Infrastructure</h1>
            <div style={{background: 'white', padding: '20px', borderRadius: '8px'}}>
                <h2>Real-time Analysis</h2>
                {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
            </div>
        </div>
    );
}
