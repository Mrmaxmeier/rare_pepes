import React, { Component } from 'react';
import { Image, Dimmer, Loader } from 'semantic-ui-react';

export class PepeImage extends Component {
  state = {
    loading: false,
    current: 'http://i3.kym-cdn.com/photos/images/original/000/862/065/0e9.jpg',
  }
  render() {
    const pepe = this.state.current;
    return (
      <div className="pepe">
        <Dimmer active={this.state.loading}>
            <Loader />
        </Dimmer>
        <Image src={pepe} fluid>
        </Image>
      </div>
    )
  }
}
