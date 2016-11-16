import React, { Component } from 'react';
import './App.css';
import { Navbar } from './Navbar.js';
import { VotingLayout } from './VotingLayout.js';
import 'semantic-ui-css/semantic.css';

export class App extends Component {
  render() {
    const store = this.props.store;
    const state = store.getState();
    return (
      <div>
        <Navbar store={store} />
        {state.page === 'home' ? <VotingLayout /> : (
          <center style={{lineHeight: '90vh'}}>
            TODO: {state.page}
          </center>
        )}
      </div>
    );
  }
}
