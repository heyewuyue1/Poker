import React from 'react';

const Card = ({ vs }) => {

    if (vs.includes('♠')) {
        var suit = 'S'
    } else if (vs.includes('♥')) {
        suit = 'H'
    } else if (vs.includes('♣')) {
        suit = 'C'
    } else if (vs.includes('♦')) {
        suit = 'D'
    }
    if (vs.length > 2) {
        var value = vs[6].toUpperCase()
    }
    else value = vs[1].toUpperCase()

    // 构建图片路径，假设所有图片都放在public/assets/cards/目录下
    const imagePath = `cards/${value}${suit}.svg`;

    return vs === '' ? (
    <div>
        <div style={{ width: '100px', height: '150px', border: '1px solid black', borderRadius: '10px', display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '5px' }}>
            
        </div>
    </div>): (
        <div style={{ width: '100px', height: '150px', margin: '5px', borderRadius: '10px', overflow: 'hidden' }}>
            <img src={imagePath} alt={`${value} of ${suit}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
    );
};

export default Card;
