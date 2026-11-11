import '@testing-library/jest-dom/vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from '../src/App.js';

function renderRoute(route: string) {
  return render(<MemoryRouter initialEntries={[route]}><App /></MemoryRouter>);
}

const capabilities = [
  { route: '/activities', empty: { activities: [] }, emptyText: /no activities/i },
  { route: '/teams', empty: { teams: [] }, emptyText: /no teams/i },
  { route: '/leaderboard', empty: { leaderboard: [] }, emptyText: /no (leaderboard|rankings|scores)/i },
  { route: '/users', empty: { users: [] }, emptyText: /no users/i },
  { route: '/workouts', empty: { workouts: [] }, emptyText: /no workouts/i },
];

describe('OctoFit presentation contract', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  beforeEach(() => {
    vi.restoreAllMocks();
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/activities/')) return new Response(JSON.stringify({ results: [{ type: 'run', minutes: 30, points: 30 }] }), { status: 200 });
      if (url.includes('/api/teams/')) return new Response(JSON.stringify([{ name: 'Octocats', members: ['Mona'] }]), { status: 200 });
      if (url.includes('/api/leaderboard/')) return new Response(JSON.stringify({ leaderboard: [{ teamName: 'Octocats', totalPoints: 90, rank: 1 }] }), { status: 200 });
      if (url.includes('/api/users/')) return new Response(JSON.stringify({ users: [{ name: 'Mona', email: 'mona@example.com' }] }), { status: 200 });
      if (url.includes('/api/workouts/')) return new Response(JSON.stringify({ workouts: [{ title: 'Intervals', focus: 'endurance' }] }), { status: 200 });
      return new Response(JSON.stringify({ message: 'Not found' }), { status: 404 });
    }));
  });

  it('renders activity data from the API', async () => {
    renderRoute('/activities');
    expect(screen.getByRole('heading', { name: /activities/i })).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/run/i)).toBeInTheDocument());
  });

  it('renders teams, leaderboard, users, and workouts with accessible content', async () => {
    const teams = renderRoute('/teams');
    await waitFor(() => expect(screen.getByText(/Octocats/)).toBeInTheDocument());
    teams.unmount();
    const leaderboard = renderRoute('/leaderboard');
    await waitFor(() => expect(screen.getByText(/90/)).toBeInTheDocument());
    leaderboard.unmount();
    const users = renderRoute('/users');
    await waitFor(() => expect(screen.getByText(/mona@example.com/)).toBeInTheDocument());
    users.unmount();
    renderRoute('/workouts');
    await waitFor(() => expect(screen.getByText(/Intervals/)).toBeInTheDocument());
  });

  it('provides navigation links to all REST-backed sections', () => {
    renderRoute('/');
    for (const name of ['Activities', 'Teams', 'Leaderboard', 'Users', 'Workouts']) {
      expect(screen.getByRole('link', { name })).toBeInTheDocument();
    }
  });

  it('requests the collection endpoint for each component', async () => {
    for (const route of ['/activities', '/teams', '/leaderboard', '/users', '/workouts']) {
      const screenResult = renderRoute(route);
      await waitFor(() => expect(fetch).toHaveBeenCalledWith(expect.stringMatching(new RegExp(`/api/${route.slice(1)}/$`))));
      screenResult.unmount();
    }
  });

  for (const capability of capabilities) {
    describe(capability.route, () => {
      it('announces a loading state while the API request is pending', () => {
        vi.stubGlobal('fetch', vi.fn(() => new Promise<Response>(() => {})));
        renderRoute(capability.route);
        expect(screen.getByRole('status')).toHaveTextContent(/loading/i);
      });

      it('shows a meaningful empty state', async () => {
        vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify(capability.empty), { status: 200 })));
        renderRoute(capability.route);
        await waitFor(() => expect(screen.getByText(capability.emptyText)).toBeInTheDocument());
      });

      it('announces API failures as an accessible alert', async () => {
        vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify({ message: 'Unavailable' }), { status: 503 })));
        renderRoute(capability.route);
        await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/unable|unavailable|error/i));
      });
    });
  }
});
