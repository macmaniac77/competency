interface Props {
  params: { id: string };
}

export default function SessionPage({ params }: Props) {
  return (
    <main className="p-8">
      <h1 className="text-xl font-bold">Session {params.id}</h1>
      <p>Detail placeholder.</p>
    </main>
  );
}
