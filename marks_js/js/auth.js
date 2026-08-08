async function getSession() {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

async function getProfile() {
  const session = await getSession();
  if (!session) return null;
  const { data, error } = await supabase
    .from('profiles')
    .select('*, schools(*)')
    .eq('id', session.user.id)
    .single();
  if (error) {
    console.error(error);
    return null;
  }
  return data;
}

async function login(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  return data;
}

async function logout() {
  await supabase.auth.signOut();
  window.location.href = 'index.html';
}

async function requireAuth(role) {
  const profile = await getProfile();
  if (!profile) {
    window.location.href = 'index.html';
    return null;
  }
  if (role && profile.role !== role) {
    window.location.href = profile.role === 'admin' ? 'admin.html' : 'school.html';
    return null;
  }
  return profile;
}
