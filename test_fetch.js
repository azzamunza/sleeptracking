const SUPABASE_URL = "https://nrwckhyegdkcbfbiitxz.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yd2NraHllZ2RrY2JmYmlpdHh6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMzYxMzcsImV4cCI6MjA4NzcxMjEzN30.j_4uCVEG2CoNv9n8tGJaPwZNqSuEqZUZUxxVLdGZcEo";

async function test() {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/get_practitioner_data`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        },
        body: JSON.stringify({ p_invite_id: '536895e3-03ec-4b18-91a8-16f357b81678' })
    });
    const text = await res.text();
    console.log("Status:", res.status);
    console.log("Body:", text);
}
test();
