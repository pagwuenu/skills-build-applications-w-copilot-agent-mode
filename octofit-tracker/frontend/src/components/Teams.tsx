import { CollectionState, displayValue, useCollection } from '../api/useCollection.js';
import DataTable from './DataTable.js';

export default function Teams() {
  const { records, loading, error } = useCollection('/api/teams/', 'teams', 'Teams');
  return (
    <section className="card data-card">
      <div className="card-header"><h2 className="h3 mb-0">Teams</h2></div>
      <div className="card-body">
        <CollectionState loading={loading} error={error} empty="No teams found." count={records.length} />
        {records.length > 0 && <DataTable records={records} columns={[
          { label: 'Team', render: (team) => displayValue(team, 'name') ?? 'Team' },
          { label: 'Mascot', render: (team) => displayValue(team, 'mascot') ?? '—' },
          { label: 'Members', render: (team) => Array.isArray(team.members) ? team.members.length : '—' },
        ]} />}
      </div>
    </section>
  );
}
