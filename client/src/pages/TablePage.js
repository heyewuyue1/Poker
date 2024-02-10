import React, { useState, useEffect } from 'react';
import Table from '../components/Table';
import withRouter from './withRouter';
import axios from 'axios'
import { useLocation } from 'react-router-dom';
import { Button, ButtonGroup, Input, Spacer, Checkbox } from '@nextui-org/react'


const TablePage = () => {
  const location = useLocation();
  const { seat, url } = location.state || {}; // 如果没有状态，使用空对象作为默认值
  const [tableStat, setTableStat] = useState('')
  const [betChips, setBetChips] = useState('')
  const [showPublic, setShowPublic] = useState([])
  const [hands, setHands] = useState([])
  const [actPlayer, setActPlayer] = useState(-1)
  const [pot, setPot] = useState(0)
  const [prefold, setPrefold] = useState(false)

  const handleInputChange = (setter) => (e) => setter(e.target.value);

  useEffect(() => {
    const pid = setInterval(() => {
      axios.get(url + '/s?seat=' + seat).then(
        (res) => {
          // console.log(res.data)
          setShowPublic(getShowPublic(res.data.public, res.data.tablestat))
          setHands(res.data.hand)
          if (res.data.actPlayer === seat && prefold) {
            fold()
            console.log('prefold')
          }
          setActPlayer(res.data.actPlayer)
          setPot(res.data.pot)
          var output = ''
          if (res.data.tablestat === 0) {
            output = 'Game not start.'
          }
          else {
            if (res.data.showdown_info.length !== 0) {
              output = res.data.showdown_info
            } else {
              var statList = res.data.players.map((player) => {
                if (player.name !== '') {
                  var stat = ''
                  if (player.status === 0)
                    stat = 'WAITING'
                  if (player.status === 1)
                    stat = 'MOVED'
                  if (player.status === 2)
                    stat = 'FOLDED'
                  return player.name + '[' + player.seat + '] ' + stat + '.' + player.left + ' left.'
                }
                return ''
              })

              output = statList.filter(i => i !== '').join('\n') + '\n\n'
                + "Current Pot: " + res.data.pot + '\n'
                + "Action Line:\n" + res.data.actionLine.join('\n') + '\n'
                + 'Your Stack: ' + res.data.stack + '\n'
                + 'Your Position: ' + seat + '\n'
                + 'Button: ' + res.data.btn + '\n'
            }
          }
          setTableStat(output)
        })
    }, 1000)
    return () => clearInterval(pid)
  })

  const getShowPublic = (public_cards, tablestat) => {
    if (tablestat === 2) {
      var show_public = public_cards.slice(0, 3)
    }
    else if (tablestat === 3) { show_public = public_cards.slice(0, 4) }
    else if (tablestat === 4) { show_public = public_cards.slice(0, 5) }
    return show_public
  }

  const ckeckOrCall = () => {
    axios.post(url + '/a', { seat: seat, move: 'c' })
  }

  const fold = () => {
    setPrefold(false)
    axios.post(url + '/a', { seat: seat, move: 'f' })
  }

  const bet = () => {
    axios.post(url + '/a', { seat: seat, move: 'b ' + betChips })
  }

  const bet13 = () => {
    var betSize = Math.round(pot / 3) - (Math.round(pot / 3) % 10)
    axios.post(url + '/a', { seat: seat, move: 'b ' + betSize })
  }

  const bet12 = () => {
    var betSize = Math.round(pot / 2) - (Math.round(pot / 2) % 10)
    axios.post(url + '/a', { seat: seat, move: 'b ' + betSize })
  }

  const bet23 = () => {
    var betSize = (Math.round(pot / 3) - (Math.round(pot / 3) % 10)) * 2
    axios.post(url + '/a', { seat: seat, move: 'b ' + betSize })
  }

  const bet34 = () => {
    var betSize = (Math.round(pot / 4) - (Math.round(pot / 4) % 10)) * 3
    axios.post(url + '/a', { seat: seat, move: 'b ' + betSize })
  }

  const bet11 = () => {
    axios.post(url + '/a', { seat: seat, move: 'b ' + pot })
  }

  const quit = () => {
    axios.post(url + '/a', { seat: seat, move: 'q' })
    window.close()
  }

  const preFold = (e) => {
    setPrefold(e.target.checked)
  }


  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      {/* 假设Table和Spacer是NextUI或您自己定义的组件 */}
      <Table cards={showPublic} hands={hands} />
      <Spacer y={1} />
      <textarea
        value={tableStat}
        readOnly
        style={{
          fontSize: '20px',
          lineHeight: '1.5',
          height: '500px',
          width: '500px',
          resize: 'both',
          borderColor: 'black',
          borderWidth: '1px',
          padding: '5px'
        }}
      />
      <Spacer y={1} />

      <div style={{ display: 'flex', gap: '10px' }}>
        <Button onClick={ckeckOrCall} disabled={actPlayer !== seat} color={actPlayer !== seat ? 'default' : 'primary'}>check/call</Button>
        <Button onClick={fold} disabled={actPlayer !== seat} color={actPlayer !== seat ? 'default' : 'danger'}>fold</Button>
        {/* {actPlayer === seat ?
          <Button onClick={fold} color='danger'>fold
          </Button> :
          <Checkbox onChange={preFold} checked={prefold}>
            fold（大盲别用）
          </Checkbox>
        } */}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Input onChange={handleInputChange(setBetChips)} disabled={actPlayer !== seat} style={{ padding: '10px', border: '2px solid #2196F3', borderRadius: '4px' }}></Input>
        <Button onClick={bet} disabled={actPlayer !== seat} color={actPlayer !== seat ? 'default' : 'success'}>bet</Button>
        <Button onClick={quit} disabled={actPlayer !== seat} color={actPlayer !== seat ? 'default' : 'warning'}>quit</Button>
      </div>
      <ButtonGroup>
        <Button onClick={bet13}
          disabled={actPlayer !== seat}
          color={actPlayer !== seat ? 'default' : 'success'}
          variant='ghost'
        >bet 1/3 pot</Button>
        <Button onClick={bet12}
          disabled={actPlayer !== seat}
          color={actPlayer !== seat ? 'default' : 'success'}
          variant='ghost'
        >bet 1/2 pot</Button>
        <Button onClick={bet23}
          disabled={actPlayer !== seat}
          color={actPlayer !== seat ? 'default' : 'success'}
          variant='ghost'
        >bet 2/3 pot</Button>
        <Button onClick={bet34}
          disabled={actPlayer !== seat}
          color={actPlayer !== seat ? 'default' : 'success'}
          variant='ghost'
        >bet 3/4 pot</Button>
        <Button onClick={bet11}
          disabled={actPlayer !== seat}
          color={actPlayer !== seat ? 'default' : 'success'}
          variant='ghost'
        >bet 100% pot</Button>
      </ButtonGroup>
    </div>
  );



}

export default withRouter(TablePage);
