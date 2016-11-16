import React from 'react'
import ReactDOM from 'react-dom'
import { createStore } from 'redux'

import { reducer } from './reducers'
import { App } from './components/App.js';
import './index.css';


const store = createStore(reducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
const rootEl = document.getElementById('root')

const render = () => ReactDOM.render(
  <App store={store} />,
  rootEl
)

render()
store.subscribe(render)