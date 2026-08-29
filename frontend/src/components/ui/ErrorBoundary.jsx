import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error('[ErrorBoundary]', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="chart-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 100 }}>
          <p style={{ color: 'var(--text-muted)', fontSize: 12 }}>
            ⚠️ {this.props.label || 'Component'} failed to render
          </p>
        </div>
      );
    }
    return this.props.children;
  }
}
