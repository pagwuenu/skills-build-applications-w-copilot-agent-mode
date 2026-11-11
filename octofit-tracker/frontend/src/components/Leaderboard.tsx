import { CollectionState, displayValue, useCollection } from '../api/useCollection.js';
import DataTable from './DataTable.js';

export default function Leaderboard() {
  const { records, loading, error } = useCollection('/api/leaderboard/', 'leaderboard', 'Leaderboard');
  return (
    <section className="card data-card">
      <div className="card-header"><h2 className="h3 mb-0">Leaderboard</h2></div>
      <div className="card-body">
        <CollectionState loading={loading} error={error} empty="No leaderboard rankings found." count={records.length} />
        {records.length > 0 && <DataTable records={records} columns={[
          { label: 'Rank', render: (entry) => displayValue(entry, 'rank') ?? '—' },
          { label: 'Team', render: (entry) => displayValue(entry, 'teamName', 'name') ?? 'Team' },
          { label: 'Points', render: (entry) => displayValue(entry, 'totalPoints', 'points') ?? '0' },
        ]} />}
      </div>
    </section>
  );
}
