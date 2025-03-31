#!/usr/bin/env bash
set -e

echo "Installing Switchmap-NG in editable mode..."
pip install -e .  # I install the Switchmap-NG package in editable mode to ensure dependencies are up to date.

echo "Installing Dashboard Node dependencies..."
if [ -f "dashboard/package.json" ]; then
    cd dashboard && npm install && cd ..  # I install the Node dependencies for the dashboard if package.json exists.
fi

# I copy the example config.yaml if one does not exist.
if [ ! -f "etc/config.yaml" ]; then
    echo "Copying example config.yaml into /workspace/etc..."
    cp examples/etc/config.yaml etc/config.yaml
fi

# I update config.yaml for the development environment.
sed -i 's/db_host:.*/db_host: db/' etc/config.yaml  # I set the database host to "db".
sed -i 's/db_user:.*/db_user: switchmap/' etc/config.yaml  # I set the database user to "switchmap".
sed -i 's/db_pass:.*/db_pass: switchmap/' etc/config.yaml  # I set the database password to "switchmap".

# (Optional) I ensure the database schema is created if the server doesn't auto-create it.
# I run SQLAlchemy's create_all via a short Python snippet:
python - <<'PYCODE'
import switchmap.server.db.models as models
from switchmap.server.db.database import ENGINE
models.Base.metadata.create_all(ENGINE)
PYCODE

echo "Devcontainer post-create setup complete."
