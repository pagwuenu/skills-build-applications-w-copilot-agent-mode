import { CollectionState, displayValue, useCollection } from '../api/useCollection.js';
import DataTable from './DataTable.js';

export default function Activities() {
  const { records, loading, error } = useCollection('/api/activities/', 'activities', 'Activities');
  return (
    <section className="card data-card">
      <div className="card-header"><h2 className="h3 mb-0">Activities</h2></div>
      <div className="card-body">
        <CollectionState loading={loading} error={error} empty="No activities found." count={records.length} />
        {records.length > 0 && <DataTable records={records} columns={[
          { label: 'Activity', render: (activity) => displayValue(activity, 'type') ?? 'Activity' },
          { label: 'Minutes', render: (activity) => displayValue(activity, 'minutes') ?? '—' },
          { label: 'Points', render: (activity) => displayValue(activity, 'points') ?? '—' },
        ]} />}
      </div>
    </section>
  );
}
