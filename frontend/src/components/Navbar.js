import React, { Component } from 'react';
import { Menu } from 'semantic-ui-react';

export class Navbar extends Component {
  handleItemClick = (e, { name }) => {
    this.props.store.dispatch({ type: 'SET_PAGE', page: name})
  }

  render() {
    let state = this.props.store.getState()
    let active = state.page
    return (
      <Menu inverted style={{borderRadius: 0}}>
        <Menu.Item name='home' active={active === 'home'} onClick={this.handleItemClick} />
        <Menu.Item name='hall_of_rareness' active={active === 'hall_of_rareness'} onClick={this.handleItemClick} />
        <Menu inverted floated='right'>
          <Menu.Item as='a' href='https://imgur.com/a/U2dTR'>rare pepes, do not steel</Menu.Item>
          <Menu.Item name='pepecount'>{state.stats.pepe || ' - '} pepes</Menu.Item>
          <Menu.Item name='votes'>{state.stats.pepe || ' - '} votes</Menu.Item>
        </Menu>
      </Menu>
    )
  }
}