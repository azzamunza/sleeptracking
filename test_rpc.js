const { createClient } = require('@supabase/supabase-js');
const SUPABASE_URL = "https://nrwckhyegdkcbfbiitxz.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yd2NraHllZ2RrY2JmYmlpdHh6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMzYxMzcsImV4cCI6MjA4NzcxMjEzN30.j_4uCVEG2CoNv9n8tGJaPwZNqSuEqZUZUxxVLdGZcEo";
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function test() {
    const { data, error } = await supabase.rpc('get_practitioner_data', { p_invite_id: '536895e3-03ec-4b18-91a8-16f357b81678' });
    console.log("Error:", error);
    console.log("Data:", data);
}
test();
