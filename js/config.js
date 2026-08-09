// ========== SUPABASE CONFIG ==========
// Paste your keys from Supabase → Project Settings → API
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

// Demo mode = true when keys not set (preview without database)
const DEMO_MODE = (SUPABASE_URL === 'YOUR_SUPABASE_URL');

let supabase = null;

function initSupabase() {
  if (!DEMO_MODE && typeof window.supabase !== 'undefined') {
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return true;
  }
  return !DEMO_MODE;
}
