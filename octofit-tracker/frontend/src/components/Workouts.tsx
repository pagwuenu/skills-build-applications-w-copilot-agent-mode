import { CollectionState, displayValue, useCollection } from '../api/useCollection.js';
import DataTable from './DataTable.js';

export default function Workouts() {
  const { records, loading, error } = useCollection('/api/workouts/', 'workouts', 'Workouts');
  return (
    <section className="card data-card">
      <div className="card-header"><h2 className="h3 mb-0">Workouts</h2></div>
      <div className="card-body">
        <CollectionState loading={loading} error={error} empty="No workouts found." count={records.length} />
        {records.length > 0 && <DataTable records={records} columns={[
          { label: 'Workout', render: (workout) => displayValue(workout, 'title', 'name') ?? 'Workout' },
          { label: 'Focus', render: (workout) => displayValue(workout, 'focus') ?? '—' },
          { label: 'Description', render: (workout) => displayValue(workout, 'description') ?? '—' },
        ]} />}
      </div>
    </section>
  );
}
