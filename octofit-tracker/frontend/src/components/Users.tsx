import { CollectionState, displayValue, useCollection } from '../api/useCollection.js';
import DataTable from './DataTable.js';

export default function Users() {
  const { records, loading, error } = useCollection('/api/users/', 'users', 'Users');
  return (
    <section className="card data-card">
      <div className="card-header"><h2 className="h3 mb-0">Users</h2></div>
      <div className="card-body">
        <CollectionState loading={loading} error={error} empty="No users found." count={records.length} />
        {records.length > 0 && <DataTable records={records} columns={[
          { label: 'Name', render: (user) => displayValue(user, 'name', 'username') ?? 'User' },
          { label: 'Email', render: (user) => displayValue(user, 'email') ?? '—' },
          { label: 'Fitness goal', render: (user) => displayValue(user, 'fitnessGoal') ?? '—' },
        ]} />}
      </div>
    </section>
  );
}
