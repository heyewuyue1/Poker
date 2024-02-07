import React from 'react';
import Card from './Card';

const Table = ({cards, hands}) => {
    // 示例牌，实际应用中应从游戏逻辑中获取
    if (cards === undefined)
    {
        cards = [
        ];
    }
    if (hands === undefined)
    {
        hands = [
        ];
    }
    // console.log(cards, hands)
    return (
        <>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {cards.map((card, index) => (
                <Card key={index} vs={card} />
            ))}
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {hands.map((card, index) => (
                <Card key={index} vs={card} />
            ))}
        </div>
        </>
    );
};

export default Table;
